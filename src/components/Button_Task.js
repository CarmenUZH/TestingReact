
import React from 'react';
import Button from "./Button";

const Button_Task = ({onAdd,showAdd}) => {
    const onClick=() =>{
        console.log("Click")
    }
    return (
        <div className="btn-block-main">
            <Button b_col ={showAdd ? "#C70039": "#355C7D"} color={showAdd ? "black":"white"} text={showAdd ?  "(screaming)":"call my foken wife"} onClick={onAdd}/>
            <p> <small> pressing this button will actually kill you </small> </p>
        </div>
    )
}

export default Button_Task