using UnityEngine;

public class Target : MonoBehaviour // scriptet ska gjør at målet reagerer når det blir truffet

{
    void OnCollisionEnter(Collision collision) // Denne funksjonen kjører automatisk når noe kolliderer med objektet

    {
        if (collision.gameObject.CompareTag("Bullet")) // Sjekker om det som traff er en kule

        {
            FindFirstObjectByType<GameManager>().TargetHit(); // finne GameManager og registrere at et mål he blitt truffet

            Destroy(gameObject); // ødelegg målet etter treff

        }
    }

}
