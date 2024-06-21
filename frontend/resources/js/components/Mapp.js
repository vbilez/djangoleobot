import React from 'react'
import ReactDOM from 'react-dom';
import { Map as LeafletMap, TileLayer, Marker, Popup } from 'react-leaflet';
import SearchLeaflet from './SearchLeaflet';
import SearchComponentLeaflet from './SearchComponentLeaflet';
class Mapp extends React.Component {
     constructor(props) {
    super(props);
    this.state = {
      currentPos: null
    };
    this.handleClick = this.handleClick.bind(this);
  }
    componentDidMount() {

    }
   handleClick(e){
    this.setState({ currentPos: e.latlng });
    this.props.setState({ currentPos: e.latlng });
  }

 SetPosition(obj){
    this.setState(obj);
    this.props.setState(obj);
  }

    render() {

        return (
         
            <LeafletMap onClick={this.handleClick}
            ref={(ref) => { this.map = ref; }}
                center={[49.78412883555824,24.0608990097046]}
                zoom={18}
                maxZoom={20}
                attributionControl={true}
                zoomControl={true}
                doubleClickZoom={true}
                scrollWheelZoom={true}
                dragging={true}
                animate={true}
                easeLinearity={0.35}
            >

                <TileLayer
                    url='http://{s}.tile.osm.org/{z}/{x}/{y}.png'
                />
                <SearchComponentLeaflet map={this.map} placeholder={"Введіть адресу"} SetPosition={this.SetPosition.bind(this)}/>
                { this.state.currentPos && <Marker position={this.state.currentPos}
                onDragEnd={ (e)=> {
                    this.setState({currentPos:e.target._latlng});
                    this.props.setState({currentPos:e.target._latlng});
                    }}    
                draggable={true}
                >
                    <Popup >
                        Popup for any custom information.
                    </Popup>

                </Marker>}
            </LeafletMap>

        );
    }
}

export default Mapp;
