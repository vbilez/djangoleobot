import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import 'bootstrap/dist/css/bootstrap.css';
export default class ReactIndex extends Component {
    render() {
        return (
            <div className="container">
                <div className="row justify-content-center">
                    <div className="col-md-8">
                        <div className="card">
                            <div className="card-header">reactindex Component</div>

                            <div className="card-body">I'm an reactindex component!</div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

if (document.getElementById('reactindex')) {
    ReactDOM.render(<ReactIndex />, document.getElementById('reactindex'));
}
