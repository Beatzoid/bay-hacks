using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TrafficLightScript : MonoBehaviour
{
    public Component greenLight;
    public Component yellowLight;
    public Component redLight;
    private float timer = 0f;
    private float[] durations = { 10f, 7f, 3f };
    private Component currentLight;
    private int currentColorIndex = 0;
    private string[] colors = { "red", "green", "yellow" };
    public bool python;
    public bool direction;

    void Start()
    {
        if (direction && !python)
        {
            redLight.GetComponent<Light>().enabled = false;
            yellowLight.GetComponent<Light>().enabled = false;
            greenLight.GetComponent<Light>().enabled = false;
            currentLight = redLight;
            timer = 0f;
            currentLight.GetComponent<Light>().enabled = true;
        }
        else if (!python)
        {
            redLight.GetComponent<Light>().enabled = false;
            yellowLight.GetComponent<Light>().enabled = false;
            greenLight.GetComponent<Light>().enabled = false;
            currentLight = greenLight;
            timer = 0f;
            currentColorIndex = 1;
            currentLight.GetComponent<Light>().enabled = true;
        }
        else
        {
            redLight.GetComponent<Light>().enabled = false;
            yellowLight.GetComponent<Light>().enabled = false;
            greenLight.GetComponent<Light>().enabled = false;
            currentLight = greenLight;
            timer = 0f;
            currentLight.GetComponent<Light>().enabled = true;
        }
    }

    void Update()
    {
        if (!python)
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
    }

    public string GetCurrentColor()
    {
        return colors[currentColorIndex];
    }

    public void Switch()
    {
        if (currentLight.name == "Green Light")
        {
            currentLight.GetComponent<Light>().enabled = false;
            currentLight = yellowLight;
            currentLight.GetComponent<Light>().enabled = true;
            StartCoroutine(SwitchToRed());
        }
        else
        {
            currentLight.GetComponent<Light>().enabled = false;
            currentLight = greenLight;
            currentLight.GetComponent<Light>().enabled = true;
        }
    }

    private IEnumerator SwitchToRed()
    {
        yield return new WaitForSeconds(2f);
        currentLight.GetComponent<Light>().enabled = false;
        currentLight = redLight;
        currentLight.GetComponent<Light>().enabled = true;
    }
}