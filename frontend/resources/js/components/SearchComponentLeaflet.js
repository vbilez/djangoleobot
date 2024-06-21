import React from 'react';
import ReactLeafletSearch from "react-leaflet-search";
function myPopup(SearchInfo) {
  return(
    <Popup>
      <div>
        <p>I am a custom popUp</p>
        <p>latitude and longitude from search component: lat:{SearchInfo.latLng[0]} lng:{SearchInfo.latLng[1]}</p>
        <p>Info from search component: {SearchInfo.info}</p>
        <p>{JSON.stringify(SearchInfo.raw)}</p>
      </div>
    </Popup>
  );
}

class SearchComponentLeaflet extends React.Component {
    constructor(props){
     super(props);
     this.state = {
      currentPos: null
    }};

    SetPosition(obj){
    this.setState(obj);
    this.props.SetPosition(obj);
  }
    render(){
        return <ReactLeafletSearch 
            position="topleft" 
            provider="OpenStreetMap" 
            providerOptions={{ region: "ua", }}
            zoom={18}
            inputPlaceholder="Введіть адресу або координати"
            SetPosition={this.SetPosition.bind(this)}
            />
    }
}
export default SearchComponentLeaflet;