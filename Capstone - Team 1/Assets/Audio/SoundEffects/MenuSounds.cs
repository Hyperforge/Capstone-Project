using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MenuSounds : MonoBehaviour
{
    [SerializeField] private AudioSource[] audioSources;
    //0 is win
    //1 is click
    //2 is game start

    public void playWin()
    {
        audioSources[0].Play();
    }

    public void stopWin()
    {
        audioSources[0].Stop();
    }

    public void playClick()
    {
        audioSources[1].Play();
    }

    public void stopClick()
    {
        audioSources[1].Stop();
    }

    public void playReady()
    {
        audioSources[2].Play();
    }

    public void stopReady()
    {
        audioSources[2].Stop();
    }

    public void stopAllsounds()
    {
        foreach (AudioSource source in audioSources)
        {
            source.Stop();
        }

    }

}
