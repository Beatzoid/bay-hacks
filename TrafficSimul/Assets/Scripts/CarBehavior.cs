using UnityEngine;
using System;

[RequireComponent(typeof(Rigidbody))]
public class CarController : MonoBehaviour
{
    public TrafficLightScript trafficLight;
    public float baseMaxSpeed = 20f;
    public float baseAcceleration = 5f;
    public float baseDeceleration = 4f;
    private float baseStopDistance = 8f;
    private float baseSlowDownDistance = 20f;
    public float centerPointDistance = 0f; // Distance from the traffic light to the center point
    public float carAwarenessDist = 200f; // Distance to check for cars in front
    private float minCarDistance = 5f; // Minimum distance to keep from car in front
    public LayerMask carLayer; // Layer for raycasting to detect other cars
    public string Status;
    private Rigidbody rb;
    private float currentSpeed = 0f;
    private bool passedCenter = false;

    // Randomized driver characteristics
    private float maxSpeed;
    private float acceleration;
    private float deceleration;
    private float stopDistance;
    private float slowDownDistance;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
        rb.constraints = RigidbodyConstraints.FreezeRotation | RigidbodyConstraints.FreezePositionY;
        RandomizeDriverCharacteristics();
    }

    void RandomizeDriverCharacteristics()
    {
        float driverSkill = UnityEngine.Random.Range(0.9f, 1.1f);
        maxSpeed = baseMaxSpeed * UnityEngine.Random.Range(0.9f, 1.1f);
        acceleration = baseAcceleration * driverSkill * UnityEngine.Random.Range(0.9f, 1.1f);
        deceleration = baseDeceleration * driverSkill * UnityEngine.Random.Range(0.9f, 1.1f);
        stopDistance = baseStopDistance * (2f - driverSkill) * UnityEngine.Random.Range(0.9f, 1.1f);
        slowDownDistance = baseSlowDownDistance * (2f - driverSkill) * UnityEngine.Random.Range(0.9f, 1.1f);
    }

    void FixedUpdate()
    {
        string lightColor = trafficLight.GetCurrentColor();
        float distanceToLight = Vector3.Distance(transform.position, trafficLight.transform.position);

        //if (!passedCenter && distanceToLight <= centerPointDistance)
        //{
        //    passedCenter = true;
        //}

        float targetSpeed = maxSpeed;

        // Check for cars in front
        RaycastHit hit;
        if (Physics.SphereCast(transform.position, 0.5f, transform.forward, out hit, carAwarenessDist, carLayer))
        {
            Debug.Log("hit");
            float distanceToCar = hit.distance;
            Rigidbody carInFront = hit.rigidbody;

            if (carInFront != null)
            {
                Debug.Log("Car in front isn't null");
                float carInFrontSpeed = carInFront.velocity.magnitude;

                // Adjust target speed based on the car in front
                if (distanceToCar <= 4)
                {
                    Status = "stopping becaues of car";
                    targetSpeed = 0f; // Stop if too close
                }
                else
                {
                    Debug.Log("slowing down");
                    float timeToStop = (distanceToCar / (currentSpeed / deceleration));
                    float minDistance = timeToStop * currentSpeed / 2;
                    if (minDistance + 6 * currentSpeed - 2 * carInFrontSpeed > distanceToCar)
                    {
                        float slowDownFactor = (distanceToCar) / (minDistance + 6 * currentSpeed - 2 * carInFrontSpeed);
                        Status = "light slowdown with a " + slowDownDistance + " and a " + distanceToCar + " for " + slowDownFactor;
                        targetSpeed = Mathf.Min(targetSpeed, maxSpeed * slowDownFactor);
                    }

                }
            }
        }
            // Traffic light logic
            if (!passedCenter)
            {
                Debug.Log("not passed center"); ;
                Debug.Log(lightColor);
                if (lightColor == "red" || lightColor == "yellow") { 
                    Debug.Log("in red or yellow");
                
                    if (distanceToLight <= stopDistance)
                    {
                        Debug.Log("stopping");
                        targetSpeed = 0f;
                        Status = "stopping down because of light in front with a " + stopDistance;
                    }
                    else
                    {
                        Debug.Log("slowing down");
                        float timeToStop = (distanceToLight / (currentSpeed / deceleration));
                        float minDistance = timeToStop * currentSpeed / 2;
                        if (minDistance + 5 * currentSpeed > distanceToLight)
                        {
                            float slowDownFactor = (distanceToLight) / (minDistance + 5 * currentSpeed);
                            Status = "light slowdown with a " + slowDownDistance + " and a " + distanceToLight + " for " + slowDownFactor;
                            targetSpeed = Mathf.Min(targetSpeed, maxSpeed * slowDownFactor);
                        }

                    }
                }
             
            else
            {
                Status = "in green with " + targetSpeed;
            }

            }

            else
            {
                Debug.Log("passed the center");
            }
        


            // Calculate and apply acceleration
            float desiredAcceleration = (targetSpeed - currentSpeed) / Time.fixedDeltaTime;
            desiredAcceleration = Mathf.Clamp(desiredAcceleration, -deceleration, acceleration);

            currentSpeed += desiredAcceleration * Time.fixedDeltaTime;
            currentSpeed = Mathf.Clamp(currentSpeed, 0f, maxSpeed);

            Vector3 force = transform.forward * desiredAcceleration * rb.mass;
            rb.AddForce(force);

            rb.velocity = transform.forward * currentSpeed;

            //      Debug.Log($"Target Speed: {targetSpeed}, Current Speed: {currentSpeed}, Force: {force.magnitude}");
        }
    
}