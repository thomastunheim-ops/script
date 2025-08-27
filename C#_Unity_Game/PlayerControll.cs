using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public float moveSpeed = 5f;
    public float lookSpeed = 5f; // Øke sensetivitet
    public Camera playerCamera;
    public GameObject bulletPrefab;
    public Transform shootPoint;
    public Transform gun; 
    private CharacterController controller;
    private float rotationX = 0f;
    private float gravity = 9.81f;

    void Start()
    {
        controller = GetComponent<CharacterController>();

    }

    void Update()
    {
        if (!canMove)
        {
            return; // hvis spilleren kan bevege se, stop Update() her
        }

        MovePlayer();
        LookAround();

        if (Input.GetMouseButtonDown(0))
        {
            Shoot();
        }
    }


    void MovePlayer()
    {
        float moveX = Input.GetAxis("Horizontal") * moveSpeed;
        float moveZ = Input.GetAxis("Vertical") * moveSpeed;

        Vector3 move = transform.right * moveX + transform.forward * moveZ;
        move.y -= gravity * Time.deltaTime; // gravitasjon

        controller.Move(move * Time.deltaTime);
    }

    void LookAround()
    {
        float mouseX = Input.GetAxis("Mouse X") * lookSpeed;
        float mouseY = Input.GetAxis("Mouse Y") * lookSpeed;

        rotationX -= mouseY;
        rotationX = Mathf.Clamp(rotationX, -90f, 90f); // kamera slipper ikke

        playerCamera.transform.localRotation = Quaternion.Euler(rotationX, 0, 0);
        transform.Rotate(Vector3.up * mouseX);

        // gun beveger seg etter kamera
        if (gun != null)
        {
            gun.rotation = playerCamera.transform.rotation;
        }
    }

    void Shoot()
    {
        Vector3 screenCenter = new Vector3(Screen.width / 2, Screen.height / 2, 0);
        Ray ray = playerCamera.ScreenPointToRay(screenCenter);

        GameObject bullet = Instantiate(bulletPrefab, shootPoint.position, Quaternion.LookRotation(ray.direction));
        Rigidbody rb = bullet.GetComponent<Rigidbody>();
        rb.linearVelocity = ray.direction * 20f; // skudd går rett frem, må øke hastighet
        Destroy(bullet, 3f); // skudd forsvinner ettter 3 sek. Må endre til skudd forsvinner når det treffer målet. 
    }

    public void LockCursor()
    {
        Cursor.lockState = CursorLockMode.Locked;
        Cursor.visible = false;
    }

    public void EnableMovement()
    {
        canMove = true;
    }

    public void DisableMovement()
    {
        canMove = false;
    }

    private bool canMove = true;

}

