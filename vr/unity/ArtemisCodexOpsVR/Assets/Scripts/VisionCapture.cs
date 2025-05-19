using UnityEngine;
using System.IO;

public class VisionCapture : MonoBehaviour
{
    public Camera captureCamera;
    public KeyCode captureKey = KeyCode.C;
    void Update()
    {
        if (Input.GetKeyDown(captureKey))
            CaptureView();
    }
    public void CaptureView()
    {
        if (captureCamera == null) captureCamera = Camera.main;
        RenderTexture rt = new RenderTexture(Screen.width, Screen.height, 24);
        captureCamera.targetTexture = rt;
        Texture2D screenShot = new Texture2D(Screen.width, Screen.height, TextureFormat.RGB24, false);
        captureCamera.Render();
        RenderTexture.active = rt;
        screenShot.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);
        captureCamera.targetTexture = null;
        RenderTexture.active = null;
        Destroy(rt);
        byte[] bytes = screenShot.EncodeToPNG();
        string filename = Path.Combine(Application.persistentDataPath, "scene_capture_" + System.DateTime.Now.ToString("yyyyMMdd_HHmmss") + ".png");
        File.WriteAllBytes(filename, bytes);
        Debug.Log($"[VisionCapture] Saved: {filename}");
    }
}
