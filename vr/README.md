# Artemis CodexOps VR

All VR assets for Artemis CodexOps live here.

## Unity VR (Recommended)

- Open Unity Hub, click "Add project" and select `vr/unity/ArtemisCodexOpsVR`.
- Recommended Unity Version: **2022 LTS or newer**.
- Install **XR Plugin Management** (via Package Manager).
- Add **XR Rig** and set up XR Interaction Toolkit for VR.
- Add a Canvas and a TextMeshProUGUI element to your scene.
- Attach `ArtemisAPI.cs` to any GameObject (e.g. a manager or UI panel).
- Drag your TextMeshProUGUI object to the `statusText` field in the Inspector.
- Enter Play mode: Artemis mission data will appear in VR!

## API Integration

The `ArtemisAPI.cs` script fetches live Artemis mission data from your cloud API.
Update the URL if you self-host.

## Contributing

- Fork, add new Unity VR scenes, agents, or visualizations, PR back to `vr/unity/`.
- Optional: add a WebXR Three.js version in `vr/webxr/`.


## Contributing VR Scenes
- Fork, clone, and add Unity or WebXR assets to vr/.
- PR your scene and describe the agent/data flow.
