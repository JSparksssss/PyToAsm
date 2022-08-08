import React, { Component } from 'react';
import {Modal,Button} from "react-bootstrap";
import Logo from "../../src/static/logo.png"

class Header extends Component{
    constructor(props){
        super(props)
        this.state = {
            show:false
        }

    }
    handleShow = () =>{
        let oldValue = this.state.show;
        this.setState({
            show:!oldValue
        })
    }
    render(){
        return(
            <div>         
            <nav className="navbar navbar-light bg-dark justify-content-between">
                <a className="navbar-brand" href="#">
                    <img src={Logo} width="120" height="30" alt=""/>  
                </a>

                <Button variant="primary" onClick={()=>this.handleShow()}>
                    Show Tutorial
                </Button>
            </nav>
        
            <Modal 
            show={this.state.show} 
            onHide={()=>this.handleShow()}
            dialogClassName="tutorial-modal">
                <Modal.Header closeButton>
                    <Modal.Title>Tutorial Video</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <iframe src="https://player.vimeo.com/video/737400856?h=ad16eb8afb&amp;badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" width="958" height="500" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen title="Screen Recording 2022-08-07 at 01.31.07.mov"></iframe>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={()=>this.handleShow()}>
                    Close
                    </Button>
                </Modal.Footer>
            </Modal>
            </div>
        )
    }
}

export default Header;