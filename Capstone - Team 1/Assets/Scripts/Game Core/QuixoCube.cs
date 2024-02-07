using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Reflection;
using System.Threading;
using UnityEngine;
using UnityEngine.EventSystems;

// source for clicking ability: https://www.youtube.com/watch?v=kkkmX3_fvfQ&ab_channel=Andrew


public class QuixoCube : MonoBehaviour, IPointerClickHandler
{
    public GameObject cube;
    public QuixoClass Game;
    public int row = 0;
    public int col = 0;
    public char face = '_';
    public Material xmat; // the color of a cube owned by the x player
    public Material omat; // the color of a cube owned by the y player
    private Point _toPoint;
    public Point toPoint
    {
        get { return _toPoint; }
        set
        {
            _toPoint = value;
            _toPos = Game.getPos(_toPoint); // Ensure _toPos is updated whenever toPoint changes
        }
    }
    private Vector3 _toPos;
    public Vector3 toPos
    {
        get { return _toPos; } 
    }

    public void resetTarget()
    {
        toPoint = new Point(0, 0); 
    }


    public void OnPointerClick(PointerEventData eventData)
    {
        if (Game.canPickPiece(row, col))
        {
            //UnityEngine.Debug.Log($"Selected block ({row},{col})");
            if (!Game.moveInProgress)
            {
                cube.SetActive(false);
                Game.moveInProgress = true;
                Game.from = loc();
                Game.poss = Game.GetPossibleMoves();
            }
            else
            {
                Game.to = loc();
                if (Game.IsValidMove())
                {
                    Game.makeMove();
                }
            }
        }
        
    }

    public Point loc() { return new Point(row, col); }

    public void Face(char f)
    {
        if (f == '_') return; // Do nothing if the face character is '_'
        cube.GetComponent<MeshRenderer>().material = f == 'X' ? xmat : omat;
        face = f;
        
    }

    public void snap()
    {
        cube.transform.position = toPos;
        row = _toPoint.row;
        col = _toPoint.col;
        resetTarget();
    }
    public void step(float spd)
    {
        cube.transform.position = Vector3.MoveTowards(cube.transform.position, toPos, spd * Time.deltaTime);
    }

    public float dist()
    {
        return Vector3.Distance(cube.transform.position, toPos);
    }
}