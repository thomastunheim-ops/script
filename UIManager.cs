using UnityEngine;
using UnityEngine.SceneManagement;

public class UIManager : MonoBehaviour
{
    public GameObject startMenuCanvas;
    public GameObject menuButton;

    void Start()
    {
        Time.timeScale = 0f; // spillet skal være pausa i starten
        startMenuCanvas.SetActive(true); // viser hele menyen
        menuButton.SetActive(false); // gjemer meny is tarten
    }

    public void StartGame()
    {
        Time.timeScale = 1f; // Resumerer spiller
        startMenuCanvas.SetActive(false); // gjemmer meny
        menuButton.SetActive(true); // viser menu kanp
        FindFirstObjectByType<PlayerController>().LockCursor(); // Lock musen
        FindFirstObjectByType<PlayerController>().EnableMovement(); // tar på bevegelse
        FindObjectOfType<MissionMessage>().ShowMission(); // starte teksten

    }


    public void OpenMenu()
    {
        Time.timeScale = 0f; // Pause
        startMenuCanvas.SetActive(true); // viser full meny
        menuButton.SetActive(false); // gjeem meny knappen
        Cursor.lockState = CursorLockMode.None; // Unlock mus
        Cursor.visible = true; // vis mus

        FindFirstObjectByType<PlayerController>().DisableMovement(); // stopper bevegelse
    }


    public void RestartGame()
    {
        Time.timeScale = 1f;
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
    }

    public void ExitGame()
    {
        Application.Quit();
        Debug.Log("Exiting game...");
    }
}
