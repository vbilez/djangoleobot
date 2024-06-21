<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="csrf-token" content="{{ csrf_token() }}">
        <title>Обмінник нерухомості</title>

        <!-- Fonts -->
       <!-- <link href="https://fonts.googleapis.com/css?family=Nunito:200,600" rel="stylesheet">-->
        
        <!-- Styles -->
        <link  rel="stylesheet" href="{{ mix('css/app.css')}}">
        <link
  rel="stylesheet"
  href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css"
  integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
  crossorigin=""
/>
        <style>


.fd-row{
    flex-direction:row;
}
.liinline{
 display:inline;
}

.my-spacer {
    flex: 1 1 auto;
}
.filler{
    flex-grow:1;
    text-align:center;
}
.flex-topmenu{
    display: flex;
    list-style: none;
    padding-left: 15px;
    padding-right: 15px;
    justify-content: space-between;
}
.flex-item-topmenu {
  padding: 5px;
  flex-basis: 15%;
  height:100%;
 }
.flex-container-inner {

  padding: 0;
 
  list-style: none;
  
  display: -webkit-box;
  display: -moz-box;
  display: -ms-flexbox;
  display: -webkit-flex;
  display: flex;
  
  row-gap: 5px;
  width:100%;
  background-color: #eeeeee;
  padding-left: 15px;
  padding-top: 15px;
  padding-bottom: 15px;
  padding-right: 15px;
  height:78px;
  justify-content:space-between;
}

.flex-item {
  padding: 10px;
  flex-basis:50%;

}

.flex-item-right {
  padding: 5px;
  flex-basis:5%;
  margin-right:auto;
}
.flex-item-desktop {
  margin-top:50px;
}
.flex-item-mobile{
   /* margin-top: 70px;*/
}

.flex-item-plus {
  padding: 5px;
  flex-basis: 20%;
  margin: auto;

  margin-top: -35px;
  margin-left: 40%;
}

.flex-item-menu {
  flex-basis: 20%;
}
.flex-item1 {
  padding: 5px;


  flex-shrink:1;
  flex-basis:100%;

  text-align: left;

}

.topmenu{
    /*height:12%;*/
    width:100%;
    background-color: #757575;
}

.image-novi{
    max-width:500px;
    height:100%;
}

.image-item{
   /*height:48px;*/

}
.image-item-zoomed{
   height:50%;
}
.image-item-backmenu{
   margin-top:50%;
   height:50%;
   padding:1px;

}
.popyt{
    margin-top:70px;
    z-index:2;
}
.propozicia{
    padding-right:100px;
}
.propozicial{
    padding-left:100px;
}
.image-item-topmenu{
   height:100%;
   width:50px; 
}

                    .item {
                        height:100%;
                        width:100px;
                        position: relative;
                        padding: 2px;
                        box-sizing: border-box;

               
                    }
                    .item2 {
                        height:100%;
                        position: relative;
                        box-sizing: border-box;
                   
                       
                    }
                    
                    .topbar {
                        width:100%;
                        height:15%;
                        background-color:#eeeeee;
                        display:flex;
                        align-items:start;
                        justify-content:start;
                        padding:7px;
      
                }

                @media(max-width: 2000px) {
                    .item2{
                        flex-basis:20%;
                        margin-left:30px;

                    }
                    .flex-container-inner{
                        -webkit-flex-flow: row;
                        height:15%;
                     }
                    .flex-item{
                        flex-basis:6%;

                    }
                    .flex-item1{
                        flex-basis:33%;    
                    }
                    .image-novi{
                     
                        height:105%;
                    }

                    .firstlist{
                        margin-left:25px;
                    }
                    .image-item {
                        height: 100%;
                    }
                }
                @media(max-width: 1333px) {
                    .item2{
                            flex-basis:50%;
                        }

                    .flex-container-inner{
                        -webkit-flex-flow: row;
                        flex-flow: row;
                        height:13%;
            
 
                    }
                    .flex-item{
                        flex-basis:9%;
                    }
                    .flex-item1{
                        flex-basis:30%;    
                    }
                    .image-novi{
       
                        height:85%;
                    }
                    .image-item{
                        height:100%;
                       
                     
                    }
                    .firstlist{
                        margin-left:25px;
                    }
                    
                }
     
                @media(min-width: 1000px) {
                    .topmenu{
                        display:none;
                    }
                    .flex-container-inner{
                        background-color: #757575;
                        padding-right:0;
                    }
                    .flex-item-plus {
                        margin-left:0;
                        margin:inherit;
                    }

                    .flex-item-desktop{
                        display:none;   
                    }
                    .flex-item-plus {
                        padding: 20px;
                        flex-basis:6%;
                    }

                    .flex-item-menu {

                        flex-basis:14%;
                    }

                    
                }

                    @media(max-width: 999px) {
                        .hiddenmap{
                            visibility:hidden;
                        }
                        .flex-container-inner{
                            {{ Request::is('addform') ? 'display:none;' : '' }}
                        }
                        .item {
                            flex-basis: 49%;
                            height: 190px;
                            align-self: center;
                        }
                        .item:nth-child(even) {
                        
                            flex: 0 0 50px;
                            flex-basis: 49%;
                            height: 190px;
                        }
                        .item2{
                            flex-basis:100%;
                        }
                        .topbar {
                            height: 100%;
                            justify-content: center;
                        }
                        .flex-container-inner{
                            -webkit-flex-flow: row wrap;
                            flex-flow: row wrap;
                            height:93%;
                        }
                        .flex-item{
                        flex-basis:50%;    
                        }
                        .flex-item1{
                            flex-basis:100%;    
                            padding-left:0 !important;
                            padding-right:0 !important;
                        }
                        .image-novi{
                            max-width:initial;
                            height:initial;
                        }
                        .image-item{
                            height:initial;
                        }
                        .firstlist{
                            margin-left:initial;
                        }
                        .flex-item-desktop{
                            margin-top:0;
                        }
                        .flex-item-menu {
                            margin-top:-29px;
                        }
                        .flex-item-mobile{
                            display:none;
                        }
     
                    }
                    @media(max-width: 320px) {
                        .item {
                            flex-basis: 49%;
                            height: 190px;
                        }
                        .item2{
                            flex-basis:100%;
                        }
                        .item:nth-child(odd) {
                            flex: 0 0 50px;
                            flex-basis: 50%;
                            height: 190px;
                        }
                        .topbar {
                            height: 100%;
                        }
                        .flex-container-inner{
                            -webkit-flex-flow: row wrap;
                            flex-flow: row wrap;
                            height:100%;
                            {{ Request::is('addform') ? 'display:none;' : '' }}
                        }
                        .flex-item{
                        flex-basis:50%;    
                        }
                        .flex-item1{
                            flex-basis:100%;   
                            padding-left:0 !important;
                            padding-right:0 !important; 
                        }
                        .image-novi{
                            max-width:initial;
                            height:initial;
                        }
                        .image-item{
                            height:initial;
                        }
                        .firstlist{
                            margin-left:initial;
                        }
                        .flex-item-desktop{
                            margin-top:0;

                        }

                        .flex-item-menu {
                            margin-top:-29px;
                        }
                        .flex-item-mobile{
                            display:none;
                        }
                
                    }
                

                .item + .item {
                    margin-left: 1px;
                }
                
                #map {
                    height: 400px;  /* The height is 400 pixels */
                    width: 100%;  /* The width is the width of the web page */
                }
            html, body {
                background-color: #fff;
                color: #636b6f;
                font-family: 'Ubuntu Medium', sans-serif;
                font-weight: 200;
                height: 100vh;
                margin: 0;
            }

            .full-height {
                height: 100vh;
            }

            .flex-center {
                align-items: center;
                display: flex;
                justify-content: center;
            }

            .position-ref {
                position: relative;
            }

            .top-right {
                position: absolute;
                right: 10px;
                top: 18px;
            }

            .content {
                text-align: center;
            }

            .title {
                font-size: 84px;
            }

            .links > a {
                color: #636b6f;
                padding: 0 25px;
                font-size: 13px;
                font-weight: 600;
                letter-spacing: .1rem;
                text-decoration: none;
                text-transform: uppercase;
            }

            .m-b-md {
                margin-bottom: 30px;
            }
        </style>
    </head>
    <body>
     <!--
    <div id="map"></div>
    <input type="text" id="searchfield" placeholder="Введіть локацію" style="width:400px">
    <div id="mapSearchInput"></div>
    <div id="mapErrorMsg"></div>
    -->
    <script>
// Initialize and add the map

function initMap() {
  // The location of Uluru
  var uluru = {lat: 49.78412883555824, lng: 24.0608990097046};
  // The map, centered at Uluru
  var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 17, center: uluru});
  // The marker, positioned at Uluru
  var marker = new google.maps.Marker({position: uluru, map: map,draggable:true});

  marker.addListener('dragend', function() 
    {
        geocodePosition(marker.getPosition());
    });

    var defaultBounds = new google.maps.LatLngBounds(
      new google.maps.LatLng(49.920355729316384, 23.916209926605234),
      new google.maps.LatLng(49.768034092813515, 24.11259054183961));
  map.fitBounds(defaultBounds);

    var input =  document.getElementById('searchfield');
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  var searchBox = new google.maps.places.SearchBox(
    /** @type {HTMLInputElement} */(input));
  google.maps.event.addListener(searchBox, 'places_changed', function() {
    var places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }
   /* for (var i = 0, marker; marker = markers[i]; i++) {
      marker.setMap(null);
    }
    */
   
    // For each place, get the icon, place name, and location.
    markers = [];
    var bounds = new google.maps.LatLngBounds();
    for (var i = 0, place; place = places[i]; i++) {
      var image = {
        url: place.icon,
        size: new google.maps.Size(10, 10),
        origin: new google.maps.Point(10,10),
        anchor: new google.maps.Point(10, 10),
        scaledSize: new google.maps.Size(10, 10)
      };

      // Create a marker for each place.
      /*
      var marker = new google.maps.Marker({
        map: map,
        icon: image,
        title: place.name,
        position: place.geometry.location
      });

      markers.push(marker);
      */
      marker.setPosition(place.geometry.location);  
      bounds.extend(place.geometry.location);
      console.log('place changed =>' + JSON.stringify(place.name));
    }

    map.fitBounds(bounds);
    map.setZoom(17);
    map.panTo(marker.position);
    console.log('place changed' +marker.position);
  
  });
}
function geocodePosition(pos) 
{
        console.log(JSON.stringify(pos));
}

function geocodePosition2(pos) 
{
   geocoder = new google.maps.Geocoder();
   geocoder.geocode
    ({
        latLng: pos
    }, 
        function(results, status) 
        {
            if (status == google.maps.GeocoderStatus.OK) 
            {
                $("#mapSearchInput").val(results[0].formatted_address);
                $("#mapErrorMsg").hide(100);
            } 
            else 
            {
                $("#mapErrorMsg").html('Cannot determine address at this location.'+status).show(100);
            }
        }
    );
}
    </script>

        <div class="flex-container position-ref full-height" style="background-color: #eeeeee;">
            <div class="topmenu flex-topmenu" >
                <li class="flex-item-topmenu"><img  src="/img/skargy.svg" class="image-item-topmenu"/></li>
                <li class="flex-item-topmenu"><img  src="/img/propozycii.svg" class="image-item-topmenu"/></li>
            </div>
            <div class="flex-container-inner">
                <div class="flex-item1 col-md-3 col-sm-12 col-xs-12 col-lg-32">
                 <img src="/img/novi-komp.svg" class="image-novi"/>
                </div>
                
                <li class="flex-item liinline"><img  src="/img/prodam.svg" class="image-item"/></li>
                <li class="flex-item"><img  src="/img/kupliyu_1578489332.svg" class="image-item"/></li>
                <li class="flex-item"><img  src="/img/zdam.svg" class="image-item"/></li>
                <li class="flex-item"><img src="/img/vynaimu_1578489332.svg" class="image-item"/></li>

                <li id="neruxomist" class="flex-item flex-item-mobile"><a href="/addform"><img src="/img/komp-dodaty-neruxomist.svg" class="image-item"/></a></li>
                <li id="popyt" class="flex-item flex-item-mobile"><img src="/img/komp-dodaty-popyt.svg" class="image-item"/></li>

                <li id="neruxomistmobile" class="flex-item flex-item-desktop" style="visibility:hidden"><a href="/addform"><img src="/img/dodaty_nerux.svg" class="image-item"/></a></li>
                <li id="popytmobile" class="flex-item flex-item-desktop" style="visibility:hidden"><img src="/img/dod_poput.svg" class="image-item"/></li>
                <li id="dodatybutton" class="flex-item-plus flex-item-desktop"><img src="/img/dodaty.svg" class="image-item"/></li>
                <li class="flex-item-menu flex-item-desktop" style="margin:auto"><img src="/img/menu-tel.svg" class="image-item"/></li>
                <div class=" flex-item filler"></div>
                <div class="flex-item">
                <!-- Right Side Of Navbar -->
                <ul class="navbar-nav ml-auto">
                        <!-- Authentication Links -->
                        @guest
                            <li class="nav-item">
                                <a class="nav-link" href="{{ route('login') }}">{{ __('Login') }}</a>
                            </li>
                            @if (Route::has('register'))
                                <li class="nav-item">
                                    <a class="nav-link" href="{{ route('register') }}">{{ __('Register') }}</a>
                                </li>
                            @endif
                        @else
                            <li class="nav-item dropdown">
                                <a id="navbarDropdown" class="nav-link dropdown-toggle" href="#" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" v-pre>
                                    {{ Auth::user()->name }} <span class="caret"></span>
                                </a>

                                <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdown">
                                    <a class="dropdown-item" href="{{ route('logout') }}"
                                       onclick="event.preventDefault();
                                                     document.getElementById('logout-form').submit();">
                                        {{ __('Logout') }}
                                    </a>

                                    <form id="logout-form" action="{{ route('logout') }}" method="POST" style="display: none;">
                                        @csrf
                                    </form>
                                </div>
                            </li>
                        @endguest
                    </ul>
                </div>
                <div class="flex-item-right" style="display:flex;justify-content:flex-end;flex-direction:row">
                    <li class="flex-item-right flex-item-mobile "><img  src="/img/skargy.svg" class="image-item-backmenu"/></li>
                    <li class="flex-item-right flex-item-mobile"><img  src="/img/propozycii.svg" class="image-item-backmenu"/></li>
                    <li class="flex-item-right flex-item-mobile"><img src="/img/menu-komp.svg" class="image-item-backmenu"/></li>
                </div>
             </div>
             <div style="width:100%;height:85%;padding:2px;" class="col-md-12 col-sm-12 col-xs-12 col-lg-12 d-flex flex-wrap" >
                <div style="height:100%;padding:7px;display:inline-block;overflow-y: scroll;background-color: #eeeeee;min-width:400px" class="col-md-3 col-sm-12 col-xs-12 col-lg-3 flex-fill" >
                    @yield('content')
                </div>
                <div style="padding:0px;display:inline-block;background-color: #eeeeee" class="col-md-9 col-sm-12 col-xs-12 col-lg-9 flex-fill hiddenmap" >
                    @yield('map')
                </div>
            </div>
        </div>
    </body>
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.4.1.min.js"></script>

    

  <script type="text/javascript" src="js/app.js"></script>

 
  <script type="text/javascript">
       $(document).ready(function() {
        console.log('ready');
        $('#dodatybutton').click(function(){
            if ( $('#neruxomistmobile').css('visibility') == 'hidden' )
            $('#neruxomistmobile').css('visibility','visible');
            else
            $('#neruxomistmobile').css('visibility','hidden');

            if ( $('#popytmobile').css('visibility') == 'hidden' )
            $('#popytmobile').css('visibility','visible');
            else
            $('#popytmobile').css('visibility','hidden');
         });


       });
   </script>
   
  
   
<!-- <script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyABQ8h9v6a5SaqoEo7VbzTZaWtvo5J0Hi8&callback=initMap&libraries=places&region=UA"
  type="text/javascript"></script>-->
  
 <!--  <key>AIzaSyDDzx7eKBsWdk7ndHkXNvhhJS70S3_lUqA</key>-->
</html>
