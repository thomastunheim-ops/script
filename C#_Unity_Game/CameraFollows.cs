using UnityEngine;

public class CameraFollow : MonoBehaviour
{
    public Transform target;   // ka kameraet skal følge
    public Vector3 offset = new Vector3(0f, 3f, -5f); // Plassering i forhold til spilleren
    public float smoothSpeed = 5f; // kor smooth kameraet beveger seg

    void LateUpdate()
    {
        if (target == null) return;

        Vector3 desiredPosition = target.position + offset;
        transform.position = Vector3.Lerp(transform.position, desiredPosition, smoothSpeed * Time.deltaTime);

        transform.LookAt(target); // kameraet se alltid mot spilleren
    }
}
