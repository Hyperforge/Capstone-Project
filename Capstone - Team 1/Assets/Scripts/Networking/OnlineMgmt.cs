using Photon.Pun;
using Photon.Realtime;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class OnlineMgmt : MonoBehaviourPunCallbacks
{
    [SerializeField] private GameObject playerLeftGame;
    private void Start()
    {
        PhotonNetwork.AddCallbackTarget(this);
    }

    public override void OnPlayerLeftRoom(Player otherPlayer)
    {
        base.OnPlayerLeftRoom(otherPlayer);
        playerLeftGame.gameObject.SetActive(true);
        StartCoroutine(waitReturnToLobby());
    }

    IEnumerator waitReturnToLobby()
    {
        yield return new WaitForSeconds(10f);

        returnToLobby();
    }

    public void returnToLobby()
    {
        PhotonNetwork.Disconnect();
        SceneManager.LoadScene("Lobby");
    }

    private void OnDestroy()
    {
        PhotonNetwork.RemoveCallbackTarget(this);
    }
}
