using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class mainmenu : MonoBehaviour
{
    public void PlayGame ()
    {
        SceneManager.LoadScene("TeamSelection");
    }

    public void MultiPlayGame()
    {
        SceneManager.LoadScene("Loading"); //changed by CED
    }

    public void WalkThroughGame()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex + 4);
    }

    public void QuitGame()
    {
        Debug.Log("Quit");
        Application.Quit();
    } 

    public void ReturnToMenu()
    {
        SceneManager.LoadScene("Main chatMenu");
    }

    public void HelpMenu()
    {
        SceneManager.LoadScene("Help Menu");
    }
}