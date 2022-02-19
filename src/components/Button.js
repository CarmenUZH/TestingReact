import React from 'react';
import PropTypes from "prop-types"

const Button = ({color, b_col, onClick, text}) => {


    return (
       <button
           onClick={onClick}
           style={{color:color,backgroundColor:b_col}}
           className="btn"
       >
           {text}
       </button>
    )
}



Button.defaultProps={
    color: "steelblue"
}

Button.propTypes={
    text: PropTypes.string,
    color: PropTypes.string,
    onClick: PropTypes.func,

}

export default Button