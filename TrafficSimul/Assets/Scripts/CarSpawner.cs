using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarSpawner : MonoBehaviour
{
    public GameObject carPrefab;
    public Transform spawnPoint;
    public float minSpawnInterval = 2f;
    public float maxSpawnInterval = 10f;
    public int maxCarsSpawned = 10;
    public Component trafficLightScript;
    private int carsSpawned = 0;
    public Quaternion rotation;
    void Start()
    {
  //      Vector3 spawnPoint = new Vector3(-5324.71f, -1081.593f, -4590.27f);
        StartCoroutine(SpawnCars());
    }

    IEnumerator SpawnCars()
    {
        while (carsSpawned < maxCarsSpawned)
        {
            float spawnInterval = Random.Range(minSpawnInterval, maxSpawnInterval);
            yield return new WaitForSeconds(spawnInterval);

            SpawnCar();
        }
    }

    void SpawnCar()
    {
        if (carPrefab != null && spawnPoint != null)
        {
            GameObject newCar = Instantiate(carPrefab, spawnPoint.position, rotation);
            newCar.transform.rotation = transform.rotation;
            carsSpawned++;
            // Optional: You can add any additional setup for the spawned car here
            // For example, you might want to set up its CarController component
            CarController carController = newCar.GetComponent<CarController>();
            if (carController != null)
            {
                carController.trafficLight = trafficLightScript;
                // Set up any necessary properties of the CarController
                // For example: carController.trafficLight = someTrafficLight;
            }
        }
        else
        {
            Debug.LogError("Car prefab or spawn point is not set in the CarSpawner!");
        }
    }
}