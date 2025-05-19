using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using TMPro; // For text display (requires TextMeshPro package)

public class ArtemisAPI : MonoBehaviour
{
    [Header("Artemis API URL")]
    public string apiUrl = "https://artemis-codexops.fly.dev/api/artemis";

    [Header("Text Display (optional)")]
    public TextMeshProUGUI statusText; // Drag a TMP UI Text here in the Unity editor

    void Start()
    {
        StartCoroutine(GetMissionData());
    }

    IEnumerator GetMissionData()
    {
        using (UnityWebRequest req = UnityWebRequest.Get(apiUrl))
        {
            yield return req.SendWebRequest();
            if (req.result == UnityWebRequest.Result.Success)
            {
                Debug.Log("Artemis Mission Data: " + req.downloadHandler.text);
                if (statusText != null)
                    statusText.text = req.downloadHandler.text;
            }
            else
            {
                Debug.LogWarning("API error: " + req.error);
                if (statusText != null)
                    statusText.text = "Error: " + req.error;
            }
        }
    }
}
