using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Linq;
using uk.vroad.api.etc;
using UnityEngine;

[RequireComponent(typeof(Camera))]
public class SnapshotCamera : MonoBehaviour
{
    public int id;

    public float horizontalOffset;

    Socket socket;

    Camera snapCam;

    int resWidth = 256;
    int resHeight = 256;


    void Awake()
    {
        snapCam = GetComponent<Camera>();

        if (snapCam.targetTexture == null)
        {
            snapCam.targetTexture = new RenderTexture(resWidth, resHeight, 24);
        }
        else
        {
            resWidth = snapCam.targetTexture.width;
            resHeight = snapCam.targetTexture.height;
        }

        socket = FindObjectOfType<Socket>();

        StartCoroutine(RepeatedSnapshots());
    }

    IEnumerator RepeatedSnapshots()
    {
        while (true)
        {
            yield return new WaitForSeconds(1f);

            Debug.Log("Taking snapshot");

            TakeSnapshot();
        }
    }

    void TakeSnapshot()
    {
        Texture2D snapshot = new Texture2D(resWidth, resHeight, TextureFormat.RGB24, false);

        snapCam.Render();
        RenderTexture.active = snapCam.targetTexture;

        snapshot.ReadPixels(new Rect(0, 0, resWidth, resHeight), 0, 0);

        Texture2D croppedImage = ResampleAndCrop(snapshot, 270, 1080, horizontalOffset);

        byte[] bytes = croppedImage.EncodeToPNG();
        string fileName = SnapshotName();

        File.WriteAllBytes(fileName, bytes);

        socket.SendData(fileName.Split("/").Last());

        Debug.Log("Took snapshot");

    }

    string SnapshotName()
    {
        return string.Format("{0}/../../python/snapshots/{1}_{2}.jpg",
            Application.dataPath,
            id,
            DateTime.Now.ToString("yyyy-MM-dd_HH-mm-ss-fff"));
    }

    Texture2D ResampleAndCrop(Texture2D source, int targetWidth, int targetHeight, float horizontalOffset = 0.0f)
    {
        int sourceWidth = source.width;
        int sourceHeight = source.height;
        float sourceAspect = (float)sourceWidth / sourceHeight;
        float targetAspect = (float)targetWidth / targetHeight;
        int xOffset = 0;
        int yOffset = 0;
        float factor = 1;

        if (sourceAspect > targetAspect)
        { // crop width
            factor = (float)targetHeight / sourceHeight;
            xOffset = (int)((sourceWidth - sourceHeight * targetAspect) * horizontalOffset);
        }
        else
        { // crop height
            factor = (float)targetWidth / sourceWidth;
            yOffset = (int)((sourceHeight - sourceWidth / targetAspect) * 0.5f);
        }

        Color32[] data = source.GetPixels32();
        Color32[] data2 = new Color32[targetWidth * targetHeight];
        for (int y = 0; y < targetHeight; y++)
        {
            for (int x = 0; x < targetWidth; x++)
            {
                var p = new Vector2(Mathf.Clamp(xOffset + x / factor, 0, sourceWidth - 1), Mathf.Clamp(yOffset + y / factor, 0, sourceHeight - 1));
                // bilinear filtering
                var c11 = data[Mathf.FloorToInt(p.x) + sourceWidth * (Mathf.FloorToInt(p.y))];
                var c12 = data[Mathf.FloorToInt(p.x) + sourceWidth * (Mathf.CeilToInt(p.y))];
                var c21 = data[Mathf.CeilToInt(p.x) + sourceWidth * (Mathf.FloorToInt(p.y))];
                var c22 = data[Mathf.CeilToInt(p.x) + sourceWidth * (Mathf.CeilToInt(p.y))];
                var f = new Vector2(Mathf.Repeat(p.x, 1f), Mathf.Repeat(p.y, 1f));
                data2[x + y * targetWidth] = Color.Lerp(Color.Lerp(c11, c12, p.y), Color.Lerp(c21, c22, p.y), p.x);
            }
        }

        var tex = new Texture2D(targetWidth, targetHeight);
        tex.SetPixels32(data2);
        tex.Apply(true);
        return tex;
    }
}
