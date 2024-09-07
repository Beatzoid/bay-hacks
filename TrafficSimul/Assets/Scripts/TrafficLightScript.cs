using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TrafficLightScript : MonoBehaviour
{
    public Component greenLight;
    public Component yellowLight;
    public Component redLight;
    private float timer = 0f;
    private float[] durations = { 3.5f, 3.5f, 1f };
    private Component currentLight;
    private int currentColorIndex = 0;
    private Color[] colors = { Color.red, Color.green, Color.yellow };
    // Start is called before the first frame update
    void Start()
    {
        redLight.GetComponent<Light>().enabled = false;
        yellowLight.GetComponent<Light>().enabled = false;
        greenLight.GetComponent<Light>().enabled = false;
        currentLight = redLight;
        timer = 2f;
        currentLight.GetComponent<Light>().enabled = true;

    }

    // Update is called once per frame
    void Update()
    {
        timer += Time.deltaTime;

        if (timer >= durations[currentColorIndex])
        {
            timer = 0f;
            currentColorIndex = (currentColorIndex + 1) % colors.Length;
            currentLight.GetComponent<Light>().enabled = false;
            if (currentLight.name == "Green Light")
            {
                currentLight = yellowLight;
            }
            else if (currentLight.name == "Yellow Light")
            {
                currentLight = redLight;
            }
            else
            {
                currentLight = greenLight;
            }
            currentLight.GetComponent<Light>().enabled = true;
        }
    }
    public Color GetCurrentColor()
    {
        return colors[currentColorIndex];
    }
}
