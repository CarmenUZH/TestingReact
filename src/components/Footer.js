import PropTypes from "prop-types"
import Button from "./Button";
import React from 'react';

const Footer = () => {
    const onClick=() =>{
        console.log("Click")
    }
    return (
       <footer className="footer">
           <p style={{color:"royalblue"}}> i cant fockin drive mate</p>
           <a href="/about">About</a>
       </footer>
    )
}

export default Footer