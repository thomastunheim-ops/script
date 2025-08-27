using UnityEngine;
using TMPro;

public class MissionMessage : MonoBehaviour
{
    public TextMeshProUGUI missionText;  // Dra inn tekst
    public float displayTime = 10f;      // Hvor lenge teksten skal vises (sekunder)

    private void Start()
    {
        missionText.gameObject.SetActive(false); // Skjul tekst ved start
    }

    public void ShowMission()
    {
        missionText.gameObject.SetActive(true); // Vis teksten
        Invoke("HideMission", displayTime);     // Skjul teksten eter X sekunder
    }

    void HideMission()
    {
        missionText.gameObject.SetActive(false); // skjuler teksten
    }
}
