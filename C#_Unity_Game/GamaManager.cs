using UnityEngine;
using TMPro;


public class GameManager : MonoBehaviour
{
    public int targetsHit = 0;            // Antall mål som spilleren he truffet
    public int totalTargets = 7;          // totalt antall mål som ska treffes
    public TextMeshProUGUI counterText;   // UI tekst som viser antall treff på skjermen
    public Camera firstPersonCamera;      // Førstepersons kamera 
    public Camera thirdPersonCamera;      // Tredjepersons kamera 

    void Start()
    {
        UpdateCounter(); // oppdaterer teksten ved start av spillet
    }

    void Update()
    {
        if (Input.GetKey(KeyCode.Escape))
        {
            Application.Quit();
        }
    }


    // Kalle den hver gang et mål blir truffet
    public void TargetHit()
    {
        targetsHit++;      // øke antall treff med 1
        UpdateCounter();   // pppdaterer tekst på skjermen

        
        if (targetsHit >= totalTargets)
        {
            WinGame(); // kjøre vinner funksjonen
        }
    }

    // Oppdaterer teksten som viser hvor mange mål som er truffet
    void UpdateCounter()
    {
        counterText.text = "Blinker truffet: " + targetsHit + " / " + totalTargets;
    }

    // kalles når spilleren har truffet alle målene sine
    void WinGame()
    {
        counterText.text = "Du klarte det!"; // Viser gratulasjonsteksten

        // sstarter seiersanimasjonen
        Animator playerAnim = FindFirstObjectByType<PlayerController>().GetComponent<Animator>();
        playerAnim.SetTrigger("Win");

        // bytte fra førstepersons kamera til tredjepersons kamera
        firstPersonCamera.enabled = false;
        thirdPersonCamera.enabled = true;
    }
}
