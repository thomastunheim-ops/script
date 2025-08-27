using UnityEngine;
using UnityEngine.AI;

public class DogFollow : MonoBehaviour
{
    public Transform player;             // Referanse til spillerens posisjon
    public float followRadius = 4f;       // kor nærme spilleren hunden skal holde seg
    public float moveCooldown = 1.5f;     // kor ofte hunden velger et nytt mål i sekond

    private NavMeshAgent agent;           // hundens NavMeshAgent
    private float cooldownTimer;          // Tid før neste mål kan velgast

    void Start()
    {
        agent = GetComponent<NavMeshAgent>(); // henter NavMeshAgent

        if (player == null)
            player = GameObject.FindGameObjectWithTag("Player").transform; // finne spilleren automatisk hvis det ikke er satt før
    }

    void Update()
    {
        if (!player) return; // vis det ikke finnes en spiller, gjør den ingenting

        cooldownTimer -= Time.deltaTime; // Teller ned tid til neste bevegelse

        // vis tiden er ute eller hunden har nådd destinasjonen
        if (cooldownTimer <= 0f || agent.remainingDistance < 0.5f)
        {
            Vector2 randomOffset = Random.insideUnitCircle * followRadius; // den velger et tilfeldig punkt innenfor en sirkel rundt spilleren
            Vector3 targetPos = player.position + new Vector3(randomOffset.x, 0, randomOffset.y); // Lager nytt mål i verden

            // Sjekker om punktet er på NavMesh
            if (NavMesh.SamplePosition(targetPos, out NavMeshHit hit, followRadius, NavMesh.AllAreas))
                agent.SetDestination(hit.position); // Sette ny destinasjon til et punkt på NavMesh som funke

            cooldownTimer = moveCooldown; // starter nedtellingen på nytt
        }
    }
}
