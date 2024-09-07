using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class CarController : MonoBehaviour
{
    public TrafficLightScript trafficLight;
    public float maxSpeed = 20f;
    public float acceleration = 5f;
    public float deceleration = 4f;
    public float stopDistance = 5f;
    public float slowDownDistance = 20f;
    public float centerPointDistance = 0f; // Distance from the traffic light to the center point

    private Rigidbody rb;
    private float currentSpeed = 0f;
    private bool passedCenter = false;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
        rb.constraints = RigidbodyConstraints.FreezeRotation | RigidbodyConstraints.FreezePositionY;
    }

    void FixedUpdate()
    {
        Color lightColor = trafficLight.GetCurrentColor();
        float distanceToLight = Vector3.Distance(transform.position, trafficLight.transform.position);

        // Check if we've passed the center point
        if (!passedCenter && distanceToLight <= centerPointDistance)
        {
            passedCenter = true;
        }

        if (!passedCenter)
        {
            if (lightColor == Color.green)
            {
                // Accelerate
                currentSpeed = Mathf.Min(currentSpeed + acceleration * Time.fixedDeltaTime, maxSpeed);
            }
            else if (lightColor == Color.yellow || lightColor == Color.red)
            {
                if (distanceToLight <= stopDistance)
                {
                    // Stop at the light
                    currentSpeed = 0f;
                }
                else if (distanceToLight <= slowDownDistance)
                {
                    // Calculate a speed reduction factor based on distance
                    float slowDownFactor = (distanceToLight - stopDistance) / (slowDownDistance - stopDistance);
                    float targetSpeed = maxSpeed * slowDownFactor;

                    // Gradually reduce speed
                    currentSpeed = Mathf.Max(currentSpeed - deceleration * Time.fixedDeltaTime, targetSpeed);
                }
            }
        }
        else
        {
            // Always accelerate after passing the center
            currentSpeed = Mathf.Min(currentSpeed + acceleration * Time.fixedDeltaTime, maxSpeed);
        }

        // Move the car forward using Rigidbody
        rb.velocity = transform.forward * currentSpeed;
    }
}