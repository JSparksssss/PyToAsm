import React, { Component } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

class Footer extends Component{
    constructor(props){
        super(props)
    }
    render(){
        return(
            <footer className="text-right text-lg-start text-white bg-dark">
                <hr className="my-3"/>
                <div className='text-center'>Mengqi Jiang from University of Glasgow</div>
                <div className='text-center'>
                    <a className="btn btn-outline-light btn-floating m-1 text-white text-right" role="button" href='https://github.com/JSparksssss'>
                        <i className="fa-brands fa-github"></i>
                    </a>
                    <span className='text-light'> @Jsparksssss</span>
                </div>
          </footer>
        )
    }
}

export default Footer;