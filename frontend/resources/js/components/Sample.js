import React, { Component } from 'react';
import ReactDOM from 'react-dom';

export default class Sample extends Component {
    render() {
        return (
            <div className="container">
                <div className="row justify-content-center">
                    <div className="col-md-8">
                        <div className="card">
                            <div className="card-header">Sample Component</div>

                            <div className="card-body">I'm an sample component!</div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

if (document.getElementById('sample')) {
    ReactDOM.render(<Sample />, document.getElementById('sample'));
}

