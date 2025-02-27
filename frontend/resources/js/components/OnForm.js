import React, { Component, RadioButton, Fragment } from 'react';
import ReactDOM from 'react-dom';
import { Formik} from 'formik';
import * as Yup from 'yup';
import {Container, TextField, FormGroup, Button, RadioGroup, Select, 
        MenuItem, Box, FormControl, Radio,FormControlLabel, Grid, Checkbox
} from '@material-ui/core';

import {Autocomplete} from '@material-ui/lab';
import Axios from 'axios';

import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';

import InputMask from "react-input-mask";
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Typography from '@material-ui/core/Typography';
import { DatePicker,MuiPickersUtilsProvider } from "@material-ui/pickers";
import DateFnsUtils from '@date-io/date-fns';
import ruLocale from "date-fns/locale/ru";
import LocationFieldsOn from './LocationFieldsOn';
import BudivliaFields from './BudivliaFields';
import TexxarakterFields from './TexxarakterFields';
import DiliankaFields from "./DiliankaFields";
import KomunikaciiFields from "./KomunikaciiFields";
import ImagesUploadDraggable from "./ImagesUploadDraggable";
import Mapp from "./Mapp";
import KstspalenField from './KstspalenField';

import MultiSelectDropdown from './MultiSelectDropdown';
import CSRFToken from './csrftoken';
 const validationSchema = Yup.object().shape({
       type_real_estate: Yup.number().moreThan(0).required("Виберіть тип нерухомості"),
//     prodazh: Yup.bool().required(),
//     vydvukorystannia:Yup.number().moreThan(0).when('type_real_estate',{
//       is: 4,
//       then: fieldSchema => fieldSchema.required(),
//     }),
//     juridichnagotovnist: Yup.bool().required(),
//     
//     kadastrovyi:Yup.string().
//      when('type_real_estate',{
//       is: 3,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 5,
//       then: fieldSchema => fieldSchema.required(),
//     }),
//     korystuvannia:Yup.number().moreThan(0).
//      when('type_real_estate',{
//       is: 3,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 5,
//       then: fieldSchema => fieldSchema.required(),
//     }),
//     area_earth:Yup.number().moreThan(0).
//      when('type_real_estate',{
//       is: 3,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 5,
//       then: fieldSchema => fieldSchema.required(),
//     }),
//     budynoktype: Yup.number().moreThan(0).
//      when('type_real_estate',{
//       is: 3,
//       then: fieldSchema => fieldSchema.required(),
//     }),
//     budivliatype: Yup.number().moreThan(0).
//      when('type_real_estate',{
//       is: 1,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 2,
//       then: fieldSchema => fieldSchema.required(),
//     }),
//      poverx: Yup.number().moreThan(0).
//      when('type_real_estate',{
//       is: 1,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 2,
//       then: fieldSchema => fieldSchema.required(),
//     }),
//     kstpoverxiv: Yup.number().moreThan(0).
//      when('type_real_estate',{
//       is: 1,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 2,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 3,
//       then: fieldSchema => fieldSchema.required(),
//     }),
//     matstin: Yup.number().moreThan(0).
//      when('type_real_estate',{
//       is: 1,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 2,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 3,
//       then: fieldSchema => fieldSchema.required(),
//     }),
//     kstspalen: Yup.number().moreThan(0).
//      when('type_real_estate',{
//       is: 2,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 3,
//       then: fieldSchema => fieldSchema.required(),
//     }),
//     kstsanvuzliv: Yup.number().moreThan(0).
//      when('type_real_estate',{
//       is: 2,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 3,
//       then: fieldSchema => fieldSchema.required(),
//     }),
//      vilneplanuvannia: Yup.bool().
//      when('type_real_estate',{
//       is: 2,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 3,
//       then: fieldSchema => fieldSchema.required(),
//     }),
//       opalennia: Yup.number().moreThan(0).
//      when('type_real_estate',{
//       is: 1,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 2,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 3,
//       then: fieldSchema => fieldSchema.required(),
//     }),
//     stankim: Yup.number().moreThan(0).
//      when('type_real_estate',{
//       is: 1,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 2,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 3,
//       then: fieldSchema => fieldSchema.required(),
//     }),
//     naspunkt: Yup.string().when('type_real_estate',{
//       is: 1,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 2,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 3,
//       then: fieldSchema => fieldSchema.required(),
//     }),
//     rayon: Yup.string().when('type_real_estate',{
//       is: 1,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 2,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 3,
//       then: fieldSchema => fieldSchema.required(),
//     }),
//      vulica: Yup.string().when('type_real_estate',{
//       is: 1,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 2,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 3,
//       then: fieldSchema => fieldSchema.required(),
//     }),
//     cina: Yup.string().required("Введіть ціну"),
//     valuta: Yup.number().required(),
//     odynuci: Yup.number().required(),
//     vidnosyny: Yup.number().moreThan(0).required("Вкажіть відносини"),
//     komisija: Yup.string().when('vidnosyny', {
//         is: 1,
//         then: fieldSchema => fieldSchema.required(),
//     }),
//     komisija_beru: Yup.string().when('vidnosyny',{
//       is: 3,
//       then: fieldSchema => fieldSchema.required(),
//     }),
//     zagplosha: Yup.number().moreThan(0)
//     .when('type_real_estate',{
//       is: 1,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 2,
//       then: fieldSchema => fieldSchema.required(),
//     }).when('type_real_estate',{
//       is: 3,
//       then: fieldSchema => fieldSchema.required(),
//     })
    

 });

  //const filteredOptions = options2.filter((o) => o.link === this.state.selectedOption.value)

export default class OnForm extends Component {
  
   constructor(props) {
    super(props);
    this.leafmapref = React.createRef();
    if (document.getElementById('leafmap')) {
        ReactDOM.render(<Mapp ref={this.leafmapref} setState={this.setParentState.bind(this)}/>, document.getElementById('leafmap'));
    }
    this.state = {
      prodazh: true,
      naspunkts:[],
      vulyci:[],
      rayon:[],
      selectedOption: {},
      selectedOption2: {},
      selectedOption3: {},
      selectedOption4: {},
      selectedOptionLoc: {},
      type:0,
      objectneruxomosti:true,
      dilusiaselect:1,
      beruselect:1,
      lat:this.props.lat,
      komunikaciipanel:true,
      budivliapanel:true,
      kstpoverxivarray:[],
      avtomiscepanel:true,
      locationpanel:true,
      texxarakter:true,
      zemlyapanel:true,
      nevtags:[],
      additionalnevtags:[],
      zk:[],
      zabudovnuk:[],
      imgs:[],
      imgsback:[],
      photobud:[],
      photobudback:[],
      photoplanuvannia:[],
      photoplanuvanniaback:[],
      photozemlia:[],
      photozemliaback:[],
      currentPos:null,
      naspunktperedmistiaselect:[],
      locationselect:1,
      vulyciperedmist:[],
      selectedNaspunkt:'Львів',
      selectedRayon:'',
      selectedVulica:'',
      selectedBudynok:'',
      selectedSection:'',
      ploshasagalna:'',
      ploshakorysna:'',
      ploshakuchnia:'',
      ploshadilianku:null,
      opalennia:[],
      doisd:[],
      komunikacii:[],

    }
    
  }
 
  async componentDidMount() {
    this.state.selectedOption4=1;
   // nevtags, additionalnevtags, zk, zabudovnuk
    let [naspunkti, vul, rayons,naspunktperedmistiajson,vulyciperedmist,nevtags] = await Promise.all([
      await Axios.get('/getnaspunkt.json'),
      await Axios.get('/getvulyci.json'), 
      await Axios.get('/getrayonu.json'),
      await Axios.get('/getnaspunktperedmistia.json'),
      await Axios.get('/getvulyciperedmist.json'),
      await Axios.get('/getnevtags.json'),
      // await Axios.get('/getadditionalnevtags.json'),
      // await Axios.get('/getzk.json'),
      // await Axios.get('/getzabudovnuk.json'),
  
      
    ]);
 
    if(naspunkti.status == 200){
     this.setState({naspunkts:naspunkti.data});
    }
    if(vul.status == 200){
    
      this.setState({vulyci:vul.data});
    }
    if(rayons.status == 200){
      this.setState({rayon:rayons.data});
    }
    if(naspunktperedmistiajson.status == 200){
      this.setState({naspunktperedmistiaselect:naspunktperedmistiajson.data});
    
    }
    if(vulyciperedmist.status == 200){
      this.setState({vulyciperedmist:vulyciperedmist.data});
    
    }
    // console.log(this.state.naspunkts);
    // console.log(this.state.vulyci);
    // console.log(this.state.rayon);
    // console.log(this.state.naspunktperedmistiaselect);
     if(nevtags.status == 200){
      this.setState({nevtags:nevtags.data});
    }

    if(additionalnevtags.status == 200){
      this.setState({additionalnevtags:additionalnevtags.data});
    }

    if(zk.status == 200){
      this.setState({zk:zk.data});
    }

    if(zk.status == 200){
      this.setState({zabudovnuk:zabudovnuk.data});
    }
    
 
   }
    error(  touched, message  )  {
        if (!touched) {
          return <React.Fragment></React.Fragment>;
        }
        if (message) {
          return <React.Fragment>{message}</React.Fragment>;
        }
        return <React.Fragment>all good</React.Fragment>;
      };

    setParentState(obj) {
      this.setState(obj);  
    }
    
    render() {
      
      const outerTheme = createMuiTheme({
        palette: {
          primary: {
            light: '#b71c1c', //червоний
            main: '#b71c1c',
            dark: '#b71c1c',
            contrastText: '#fff',
          },
          secondary: {
            light: '#757575', //верхнє меню + контур активного елемента
            main: '#757575',
            dark: '#757575',
            contrastText: '#000',
          },
          tertiary: {
            light: '#bdbdbd', //контур не виділених елементів +  іконок
            main: '#bdbdbd',
            dark: '#bdbdbd',
            contrastText: '#000',
          },

          blackcolor: {
            light: '#000',
            main: '#000',
            dark: '#000',
            contrastText: '#fff',
          },
          backgroundcolor: {
            light: '#eeeeee', //фоновий колір
            main: '#eeeeee',
            dark: '#eeeeee',
            contrastText: '#fff',
          },
        },
      });
 

      const themecustom = createMuiTheme({
        overrides: {
         MuiSelect: {
            selectMenu: {
                whiteSpace: 'normal'
            }
          },
          MuiInputLabel: {
            root: {
              color: outerTheme.palette.blackcolor.light,
              fontFamily: "'Ubuntu Medium'",
              fontWeight:'bold',
              "&$focused": {
                color: outerTheme.palette.secondary.light,
                fontFamily:"'Ubuntu Medium', sans-serif",
                fontWeight:'bold',
              }
            }
          },
          MuiOutlinedInput: {
            root: {
                position: 'relative',
                '& $notchedOutline': {
                    borderColor: outerTheme.palette.tertiary.light,
                },
                '&:hover:not($disabled):not($focused):not($error) $notchedOutline': {
                    borderColor:  outerTheme.palette.tertiary.light,
                    // Reset on touch devices, it doesn't add specificity
                    '@media (hover: none)': {
                        borderColor:  outerTheme.palette.tertiary.light,
                    },
                },
                '&$focused $notchedOutline': {
                    borderColor: outerTheme.palette.secondary.light,
                    borderWidth: 1
                },
      
            },
         },
         MuiTypography: {
          body1: {
            fontFamily: "'Ubuntu Medium', sans-serif",
            fontWeight: 600
          },
         },
         MuiInputBase: {
          root: {
            
            fontFamily: "'Ubuntu Medium', sans-serif",
            fontWeight: 600,
            backgroundColor: "white"
          },
          
         },
         MuiCheckbox: {
          colorSecondary: {
            '&$checked': {
              color: outerTheme.palette.primary.main
            },
          },
         }
        }
      });

        const options1 = this.state.naspunkts;
        const options2 = this.state.rayon;
        const options3 = this.state.vulyci;
        const options4 = this.state.naspunkts;
        const options5 = this.state.vulyciperedmist;

        const filteredOptions = options3.filter((o)=>o.misto === this.state.selectedOption4);
        // const filteredOptionsLoc = options2.filter((o) => o.misto=== this.state.selectedOptionLoc);
        // const filteredOptions = options2.filter((o) => o.misto === this.state.selectedOption);
        // let filteredOptions2 =  options3.filter((o) => o.link === this.state.selectedOption);
        // const filteredOptions3 = options5.filter((o)=>o.link === this.state.selectedOption4)
        
       
        const kistpoverxiv = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30];
        const poverxy = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25];
        const countries = [
         {label:"Забудовник1"},
          {label:"Забудовник2"},
          {label:"Забудовник3"},
          {label:"Забудовник4"}
        ];

        const nevtags = this.state.nevtags;
        const additionalnevtags = this.state.additionalnevtags; 
        const zkoptions = this.state.zk;
        const zabudovnukoptions = this.state.zabudovnuk;
        const remontstyletags = [
          {id:1,label:"Стиль ремонту тест 1"},
          {id:2,label:"Стиль ремонту тест 2"},
        ];
        const marginb = 15;

      
        const handleChangePloshaSagalna = (e) => {
          let inputValue = e.target.value;
      
          // Prevent negative numbers
          if (inputValue < 0) {
            return;
          }
          if (inputValue == 0) {
            inputValue=0.01
          }
      
          // Check if the value has more than two decimal places
          if (inputValue.includes('.')) {
            const [integerPart, decimalPart] = inputValue.split('.');
            if (decimalPart.length > 2) {
              // Limit to two decimal places
              inputValue = `${integerPart}.${decimalPart.slice(0, 2)}`;
            }
          }
      
          // Update the state with the formatted value
          this.setState({ploshasagalna:inputValue});
        };

        const handleChangePloshaKorysna = (e) => {
          let inputValue = e.target.value;
      
          // Prevent negative numbers
          if (inputValue < 0) {
            return;
          }
          if (inputValue == 0) {
            inputValue=0.01
          }
      
          // Check if the value has more than two decimal places
          if (inputValue.includes('.')) {
            const [integerPart, decimalPart] = inputValue.split('.');
            if (decimalPart.length > 2) {
              // Limit to two decimal places
              inputValue = `${integerPart}.${decimalPart.slice(0, 2)}`;
            }
          }
      
          // Update the state with the formatted value
          this.setState({ploshakorysna:inputValue});
        };


        const handleChangePloshaKuchnia = (e) => {
          let inputValue = e.target.value;
      
          // Prevent negative numbers
          if (inputValue < 0) {
            return;
          }

          if (inputValue == 0) {
            inputValue=0.01
          }

      
          // Check if the value has more than two decimal places
          if (inputValue.includes('.')) {
            const [integerPart, decimalPart] = inputValue.split('.');
            if (decimalPart.length > 2) {
              // Limit to two decimal places
              inputValue = `${integerPart}.${decimalPart.slice(0, 2)}`;
            }
          }
      
          // Update the state with the formatted value
          this.setState({ploshakuchnia:inputValue});
        };
        const handleChangePloshaDilianku = (e) => {
          let inputValue = e.target.value;
      
          // Prevent negative numbers
          if (inputValue < 0) {
            inputValue=0.01
          }

          if (inputValue == 0) {
            inputValue=0.01
          }
      
          // Check if the value has more than two decimal places
          if (inputValue.includes('.')) {
            const [integerPart, decimalPart] = inputValue.split('.');
            if (decimalPart.length > 2) {
              // Limit to two decimal places
              inputValue = `${integerPart}.${decimalPart.slice(0, 2)}`;
            }
          }
      
          // Update the state with the formatted value
          this.setState({ploshadilianku:inputValue});
        };

        const handleKeyDown = (e) => {

          // Prevent decrementing if value is 0 and down arrow is pressed
          if (e.key === 'ArrowDown' && (e.target.value <= 0)) {
            e.preventDefault();
          }
        };

        const handleKeyDownPoverx = (e) => {

          // Prevent decrementing if value is 0 and down arrow is pressed
          if (e.key === 'ArrowDown' && (e.target.value <=1)) {
            e.preventDefault();
          }
        };

        const handleChangeOpalennia = (event) => {
         this.setState({opalennia:event.target.value});
        };
        const opalenniachoices = ['відсутнє', 'центральне', 'пічне', 'автономне газове', 'автономне електричне','будинкове'];
        const doisdchoices = ['відсутній', 'грунт', 'бруківка', 'асфальт'];
        const komunikaciichoices = ['світло', 'вода', 'газ', 'відсутні'];
        const handleKomunikaciiSelectionChange = (selectedOptions) => {
          this.setState({ komunikacii: selectedOptions });
        };
        const handleOpalenniaSelectionChange = (selectedOptions) => {
          this.setState({ opalennia: selectedOptions });
        };
        const handleDoisdSelectionChange= (selectedOptions) => {
          this.setState({ doisd: selectedOptions });
        };

        function getCookie(name) {
          var cookieValue = null;
          if (document.cookie && document.cookie !== '') {
              var cookies = document.cookie.split(';');
              for (var i = 0; i < cookies.length; i++) {
                  var cookie = jQuery.trim(cookies[i]);
                  if (cookie.substring(0, name.length + 1) === (name + '=')) {
                      cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                      break;
                  }
              }
          }
          return cookieValue;
      }
        return (
          
        <ThemeProvider theme={themecustom}>
        
         <Container style={{widht:"100%",height:"100%"}}>
            <Formik  
            
                initialValues={{
                 prodazh:true,type_real_estate: '', naspunkt: '', cina:'',
                 valuta:1, odynuci:1, vidnosyny: '',
                 komisija:'', osoba:1, dilusia:1, locationselect: '',
                 komisija_beru:'',beru:1,beru_hidden:true, dilusia_hidden:true,
                 rayon:'', vulica: '',budynok :'',kvartyra:'',korpus: '',kadastrovyi:'',lat:'',lng:'',svitlo:false,gaz:false,
                 budivliatype:'',korystuvannia:'',pryznachennia:'',voda:'',kanalizacia:'',kstpoverxiv:'',matstin:'',
                 matperekrytya:'',matsxodiv:'',pamyatkarx:'',databudivnyctva:null,probudivliu:'',zakrytateritoria:false,
                 klasbudivli:'',kadastrovyi_budivlia:'',planuvannia_budynku:'',stanbudivnuctva:'',zagplosha:'',korysnaplosha:'',
                 kuchniplosha:'',dush:false,vanna:false,tualet:false,poverx:'',kimnatade:'',opalennia:'',stankim:'',vxid:'',vxidv:'',
                 kstbalkoniv:'',kstrivniv:1,kstsanvuzliv:'',vilneplanuvannia:false,kstspalen:'',vydvukorystannia:'',kstvitryn:'',
                 kstrivnivmisce:1,avtomiscetype:'',poverxmisce1:'',matavtomisce:'',parkovkanavulyci:'',stanavtomisce:'',
                 remontstyle:'',landshaftnuidesign:false,remontstyletags:'',budynoktype:'',kstrivnivbudynok:'',zdachiakvartal:'',dojizd:'',
                 kstbalkonivextended:'',chergabudivnyctva:'',terminorendu:'',juridichnagotovnist:false,podatokzprodazhu:false,dodatkovoproon:'',
                 podatynaportal:true,potyzhnist:'',vxidvprymishennia:[],parkomisc:'',vysotasteli:'',area_earth:'',naspunktperedmistiaselect:'',
                 ploshasagalna:'',ploshakorysna:'',ploshakuchnia:'',
                 
                }}
                validationSchema={validationSchema}
                onSubmit = {(values, { setSubmitting, resetForm, setValues }) => {
           
                 var csrftoken =getCookie('csrftoken');
                 Axios.defaults.headers.common['X-CSRF-TOKEN'] = csrftoken;
                 setSubmitting(true);
                    
                     setTimeout(async () => {
                        alert(JSON.stringify(values,null,2));
                        //console.log(JSON.stringify(values,null,2));
                        //setFieldValue("onimages",this.state.imgs);

                      var imgs = this.state.imgs;
                      let array1= await Promise.all(imgs.map(async (element)=> {
                            const imgheader = {
                                data : element,
                                dir : 'on'
                            };
                            return axios.post('makeimage',imgheader).then((response)=> {
                              
                              return [response.data.id,response.data.imgname,response.data.dir]
                            }).catch((error) =>{
                              
                              return error;
                            });
                          }));
                          this.setState({imgsback:array1});

                          var photobud = this.state.photobud;
                          let array2= await Promise.all(photobud.map(async (element)=> {
                            const imgheader = {
                                data : element,
                                dir : 'photobud'
                            };
                            return axios.post('makeimage',imgheader).then((response)=> {
                              return response.data.id;
                            }).catch((error) =>{
                              return error;
                            });
                          }));
                          this.setState({photobudback:array2});

                          var photoplanuvannia = this.state.photoplanuvannia;
                          let array3= await Promise.all(photoplanuvannia.map(async (element)=> {
                            const imgheader = {
                                data : element,
                                dir : 'photoplanuvannia'
                            };
                            return axios.post('makeimage',imgheader).then((response)=> {
                              return response.data.id;
                            }).catch((error) =>{
                              return error;
                            });
                          }));
                          this.setState({photoplanuvanniaback:array3});



                          var photozemlia = this.state.photozemlia;
                          let array4= await Promise.all(photozemlia.map(async (element)=> {
                            const imgheader = {
                                data : element,
                                dir : 'photozemlia'
                            };
                            return axios.post('makeimage',imgheader).then((response)=> {
                              return response.data.id;
                            }).catch((error) =>{
                              return error;
                            });
                          }));
                          this.setState({photozemliaback:array3});
                          
                          var payload = {...values,
                                          "csrfmiddlewaretoken":csrftoken,
                                          "ploshasagalnaa":this.state.ploshasagalna,
                                          "ploshakorysnaa":this.state.ploshakorysna,
                                          "ploshakuchniaa":this.state.ploshakuchnia,
                                          "ploshadilianku":this.state.ploshadilianku,
                                          "poverx":document.getElementById("poverx").value,
                                          "poverxovist":document.getElementById("poverxovist").value,
                                          "rayon":this.state.selectedOption,
                                          "opalenniaa":this.state.opalennia,
                                          "doisd":this.state.doisd,
                                          "komunikacii":this.state.komunikacii,
                                          "onimages":  this.state.imgsback,
                                          "latstr":document.getElementById("lat").value,
                                          "lngstr":document.getElementById("lng").value,
                                   
                                          "photobud":  this.state.photobudback,  
                                          "photoplanuvannia":  this.state.photoplanuvanniaback,
                                          "photozemlia":  this.state.photozemliaback,
                                          "currentPos": this.state.currentPos
                                         } 
                        console.log(payload)
                        await setValues(payload);
                       


                        await axios.post('objectneruxomosti',payload).then(function (response) {
                          console.log(response);
                         // resetForm();
                        })
                        .catch(function (error) {
                          console.log(error);
                        });;
                         
                        setSubmitting(false);
                    }, 500);
                    
                }}
                
            >
                {({values, errors, touched, handleChange, handleBlur, handleSubmit, isSubmitting, setFieldValue,props}) => (
                
                  <form onSubmit={handleSubmit} >
                    <CSRFToken/>
                      {JSON.stringify(errors)
                      }
                        <FormGroup style={{display: 'flex', alignItems: 'center', justifyContent: 'center',}} >
                          <FormControl component="fieldset" >
      
                            <RadioGroup value={values.prodazh} name="prodazh" row>
                                <FormControlLabel

                                value={true}
                                control={<Radio style ={{
                                  color: outerTheme.palette.primary.light,
                                }} />}
                                label="Продам"
                                labelPlacement="end"
                                onChange={() => setFieldValue("prodazh", true) }

                                />
                                <FormControlLabel
                                value={false}
                                control={<Radio style ={{
                                  color: outerTheme.palette.primary.light,
                                }} />}
                                label="Здам"
                                labelPlacement="end"
                                onChange={() => setFieldValue("prodazh",false)}
                                />
                            </RadioGroup>

                          </FormControl>
                        </FormGroup>
                        
                       <FormGroup>
                        <FormControl>
                       
                            <TextField variant="outlined"
                                style={{marginBottom:"7px"}}
                                select
                                error={touched.type_real_estate && Boolean(errors.type_real_estate)}
                                label="Тип нерухомості"
                                name="type_real_estate"
                                id="type_real_estate"
                                value={values.type_real_estate}
                                margin={"dense"}
                                onChange={(e)=>{handleChange(e);
                                  if(e!==null)
                                  {
                                    this.setState({type:e.target.value});
                                    if(e.target.value==5)
                                    {
                                      this.setState({objectneruxomosti:false});
                                    }
                                    else
                                    {
                                      this.setState({objectneruxomosti:true});
                                    }
                                  }
                                }}

                                placeholder="Виберіть тип"
                                >


                                <MenuItem value={1}>Кімната</MenuItem>
                                <MenuItem value={2}>Квартира</MenuItem>
                                <MenuItem value={3}>Будинок</MenuItem>
                                <MenuItem value={4}>Комерція</MenuItem>
                                <MenuItem value={5}>Земля</MenuItem>
                                <MenuItem value={6}>Парковка</MenuItem>
                            </TextField>
                            
                        </FormControl>
                       </FormGroup>
                          <FormGroup hidden={values.type_real_estate!==4}>
                         <FormControl hidden={values.type_real_estate!==4} >
                              <TextField variant="outlined"
                                style={{marginBottom:"7px"}}
                                select
                                error={touched.vydvukorystannia && Boolean(errors.vydvukorystannia)}
                                label="Тип комерції"
                                name="vydvukorystannia"
                                id="vydvukorystannia"
                                value={values.vydvukorystannia}
                                margin={"dense"}
                                onChange={(e)=>{handleChange(e);
                                 
                                }}

                                placeholder="Виберіть тип комерції"
                                >
                                <MenuItem value={1}>офіс</MenuItem>
                                <MenuItem value={2}>торгівля</MenuItem>
                                <MenuItem value={3}>громадське харчування</MenuItem>
                                <MenuItem value={4}>склад</MenuItem>
                                <MenuItem value={5}>виробництво</MenuItem>
                                <MenuItem value={6}>готовий бізнес</MenuItem>
                           
                            </TextField>
                       </FormControl>
                       <FormControl hidden={values.vydvukorystannia!==6 && values.type_real_estate!==4}>
                          <Autocomplete
                            freeSolo
                            multiple
                            id="nev"
                            name="nev"
                            error={errors.nev}
                            getOptionLabel={option => typeof option === 'object' ? option.label : option}
                            placeholder="НЕВ"
                            options={nevtags}
                            renderInput={params => (
                              <TextField {...params}     label="НЕВ" variant="outlined" fullWidth margin={"dense"} />
                            )}
                            renderOption={option => (
                              <React.Fragment>
                                {typeof option === 'object' ? option.label : option}
                              </React.Fragment>
                            )}

                            onChange={(o,v)=> {
                              //handleChange(o,v);
                              o.preventDefault();
                              setFieldValue("nev",v);
                                           
                            }}
                            >
                        
                          </Autocomplete>
                          
                       </FormControl>

                       <FormControl hidden={values.type_real_estate!==4}>
                          <Autocomplete
                            freeSolo
                            multiple
                            id="additionalnevtags"
                            name="additionalnevtags"
                            error={errors.nev}
                            getOptionLabel={option => typeof option === 'object' ? option.label : option}
                            placeholder="вид використання тегами"
                            options={additionalnevtags}
                            renderInput={params => (
                              <TextField {...params}     label="Вкажіть вид використання" variant="outlined" fullWidth margin={"dense"} />
                            )}
                            renderOption={option => (
                              <React.Fragment>
                                {typeof option === 'object' ? option.label : option}
                              </React.Fragment>
                            )}
                            onChange={(o,v)=> { setFieldValue("additionalnevtags",v); }}
                            >
                        
                          </Autocomplete>
                          
                       </FormControl>
                        <FormControl  hidden={true}>
                            <TextField 
                              variant="outlined"
                              label="Кількість вітрин"
                              display="inline"
                              error={touched.kstvitryn && Boolean(errors.kstvitryn)}
                              type="number" 
                              name="kstvitryn" 
                              id="kstvitryn" 
                              margin={"dense"}
                              inputProps={{ min: "1", max: "99", step: "1" }}
                                  pattern='[0-9]{2}'
                              onKeyDown={e => {
                                    if(values.cina.length>2) return e.preventDefault();
                                    if(e.key=="+") return e.preventDefault();
                                    if(e.key=="-") return e.preventDefault();
                                    if(e.key=="Enter") return e.preventDefault();
                                    if(e.key=="e") return e.preventDefault();
                                    if(e.key=="m") return e.preventDefault();
                                    if(e.key==".") return e.preventDefault();
                                    if(e.key==",") return e.preventDefault();
                                  }}
                              onChange={(e,v)=>  { if(e.target.value.length<=2){if(e.target.value!="0")handleChange(e,v);}}} 
                              value={values.kstvitryn}
                            />
                        </FormControl>
                      </FormGroup>
                      <FormGroup hidden={true}>
                        <FormControl>
                            <FormControlLabel
                                  control={
                                    <Checkbox name="rampa"  value={values.rampa}  onClick={(event)=>{ setFieldValue("rampa",Boolean(event.target.checked));}}/>
                                  }
                                  label="Рампа"
                            />
                        </FormControl>
                        <FormControl>
                            <FormControlLabel
                                  control={
                                    <Checkbox name="zdhilka"  value={values.zdhilka}  onClick={(event)=>{ setFieldValue("zdhilka",Boolean(event.target.checked));}}/>
                                  }
                                  label="Ж/д гілка"
                            />
                        </FormControl>
                        <FormControl>
                            <FormControlLabel
                                  control={
                                    <Checkbox name="telfer"  value={values.telfer}  onClick={(event)=>{ setFieldValue("telfer",Boolean(event.target.checked));}}/>
                                  }
                                  label="Тельфер"
                            />
                        </FormControl>
                        <FormControl>
                            <FormControlLabel
                                  control={
                                    <Checkbox name="kozkran"  value={values.kozkran}  onClick={(event)=>{ setFieldValue("kozkran",Boolean(event.target.checked));}}/>
                                  }
                                  label="Козловий кран"
                            />
                        </FormControl>
                        <FormControl>
                            <FormControlLabel
                                  control={
                                    <Checkbox name="pidjizdvantazhivok"  value={values.pidjizdvantazhivok}  onClick={(event)=>{ setFieldValue("pidjizdvantazhivok",Boolean(event.target.checked));}}/>
                                  }
                                  label="Підїзд вантажівок"
                            />
                        </FormControl>
                        <FormControl>
                            <FormControlLabel
                                  control={
                                    <Checkbox name="pryleglateritoria"  value={values.pryleglateritoria}  onClick={(event)=>{ setFieldValue("pryleglateritoria",Boolean(event.target.checked));}}/>
                                  }
                                  label="Прилегла територія"
                            />
                        </FormControl>
                        <FormControl>
                            <FormControlLabel
                                  control={
                                    <Checkbox name="temperaturneobladnannia"  value={values.temperaturneobladnannia}  onClick={(event)=>{ setFieldValue("temperaturneobladnannia",Boolean(event.target.checked));}}/>
                                  }
                                  label="Температурне обладнання"
                            />
                        </FormControl>
                        
                        </FormGroup>

                       <LocationFieldsOn setState={this.setParentState.bind(this)} state={this.state} handleChange={handleChange} handleBlur={handleBlur} values={values} touched={touched} errors={errors}
                          options1={options1}  options2={options2} options3={options3} options4={options4} filteredOptions={filteredOptions} setFieldValue={setFieldValue}
                          display={true} options5={options5}
                       />


                       <FormGroup>
                       <KstspalenField setState={this.setParentState.bind(this)} state={this.state} handleChange={handleChange} handleBlur={handleBlur} values={values} touched={touched} errors={errors}
                           setFieldValue={setFieldValue}
                          display={this.state.type==1||this.state.type==2||this.state.type==3}
                       />  
                       </FormGroup>


                       <FormGroup>
                         <FormControl hidden={(values.prodazh==true && (values.type_real_estate==1||values.type_real_estate==2||values.type_real_estate==4||values.type_real_estate==6))||(values.prodazh==false&&values.type_real_estate!==5)||values.type_real_estate==''}> 
                                    <TextField variant="outlined"
                                    style={{marginBottom:"7px"}}
                                    select
                                    error={touched.prysnachenniasemli && Boolean(errors.prysnachenniasemli)}
                                    label="Призначення землі"
                                    name="prysnachenniasemli"
                                    id="prysnachenniasemli"
                          
                                    margin={"dense"}
                                    onChange={(e)=>{handleChange(e);
          
                                    }}

                                    placeholder="Призначення землі"
                                    >


                                    <MenuItem value={1}>індивідуальна забудова</MenuItem>
                                    <MenuItem value={2}>багатоквартирна забудова</MenuItem>
                                    <MenuItem value={3}>ОСГ</MenuItem>
                                    <MenuItem value={4}>торгівля</MenuItem>
                                    <MenuItem value={5}>промисловість</MenuItem>
                                    <MenuItem value={6}>садівництво</MenuItem>
                                    <MenuItem value={7}>відпочинок</MenuItem>
                                    <MenuItem value={8}>інше</MenuItem>
                                </TextField>
                           </FormControl>
                         </FormGroup>

                       <FormGroup>
                       <FormControl fullWidth hidden={values.type_real_estate==1||values.type_real_estate==4||values.type_real_estate==5||values.type_real_estate==6||values.type_real_estate==''}>
                              <TextField variant="outlined"
                                label="Будівля"
                                select
                                fullWidth
                                display="inline"
                                error={touched.budivlia && Boolean(errors.budivlia)}
                                name="budivlia"
                                id="budivlia"
                                value={values.budivlia}
                                onChange={handleChange}
                                placeholder="виберіть тип будівлі"
                                margin={"dense"}
                                >

                                <MenuItem value={1}>будується</MenuItem>
                                <MenuItem value={2}>новобудова</MenuItem>
                                <MenuItem value={3}>українська забудова біл 10р.</MenuItem>
                                <MenuItem value={4}>радянська забудова</MenuItem>
                                <MenuItem value={5}>будинок старого Львова</MenuItem>
                                <MenuItem value={6}>гуртожиток</MenuItem>
                                
                              </TextField>
                             </FormControl>
                        </FormGroup>
                        
                        <FormGroup>
                       <FormControl fullWidth hidden={values.type_real_estate!==3}>
                              <TextField variant="outlined"
                                label="Тип будинку"
                                select
                                fullWidth
                                display="inline"
                                error={touched.budynoktype && Boolean(errors.budynoktype)}
                                name="budynoktype"
                                id="budynoktype"
                  
                                onChange={handleChange}
                                placeholder="виберіть тип будинку"
                                margin={"dense"}
                                >

                                <MenuItem value={1}>особняк</MenuItem>
                                <MenuItem value={2}>спарка</MenuItem>
                                <MenuItem value={3}>таунхаус</MenuItem>
                                <MenuItem value={4}>дача</MenuItem>
                                <MenuItem value={5}>незавершений</MenuItem>

                                
                              </TextField>
                             </FormControl>
                        </FormGroup>
                        <FormGroup>

                      
                        <FormControl>
                              <FormControlLabel
                                    control={
                                      <Checkbox name="okremostojachyi"  value={values.okremostojachyi}  onClick={(event)=>{ setFieldValue("okremostojachyi",Boolean(event.target.checked));}}/>
                                    }
                                    label="Окрема будівля"
                              />
                          </FormControl>
                        </FormGroup>
                    
                                
                      
                       <DiliankaFields setState={this.setParentState.bind(this)} state={this.state} handleChange={handleChange} handleBlur={handleBlur} values={values} touched={touched} errors={errors}
                           setFieldValue={setFieldValue}
                          display={false}
                       />

                        <KomunikaciiFields setState={this.setParentState.bind(this)} state={this.state} handleChange={handleChange} handleBlur={handleBlur} values={values} touched={touched} errors={errors}
                           setFieldValue={setFieldValue}
                          display={false}
                       />
            
                        <BudivliaFields setState={this.setParentState.bind(this)} state={this.state} handleChange={handleChange} handleBlur={handleBlur} values={values} touched={touched} errors={errors}
                          kistpoverxiv={kistpoverxiv} setFieldValue={setFieldValue} zabudovnukoptions={zabudovnukoptions} zkoptions={zkoptions}
                          display={false}
                       />
               
                       <FormGroup>
                      
                          <TextField 
                           
                            variant="outlined"
                            margin="dense"
                            name="lat"
                            id="lat"
                            
                    
                          >
                          </TextField>

                          <TextField 
                         
                            variant="outlined"
                            margin="dense"
                            name="lng"
                            id="lng"
                          >
                          </TextField>
                       
                       </FormGroup>
                      <TexxarakterFields setState={this.setParentState.bind(this)} state={this.state} handleChange={handleChange} handleBlur={handleBlur} values={values} touched={touched} errors={errors}
                          kistpoverxiv={kistpoverxiv} setFieldValue={setFieldValue} countries={countries} poverxy={poverxy}
                          display={false}
                       />
                        
                        <FormGroup>
                          
                          <FormControl hidden={(values.type_real_estate==1&&values.prodazh==false)||values.type_real_estate==5||values.type_real_estate==''}>
                             <TextField 
                               variant="outlined"
                               label="Площа, загальна"
                               min={0}
                               step={0.01}
                               display="inline"
                               error={touched.ploshasagalna && Boolean(errors.ploshasagalna)}
                               type="number" 
                               name="ploshasagalna" 
                               id="ploshasagalna" 
                               margin={"dense"}
                               value={this.state.ploshasagalna}
                               onChange={handleChangePloshaSagalna}
                               onKeyDown={handleKeyDown}
                               
                             />
                             </FormControl>
                             <FormControl hidden={(values.prodazh==true&&(values.type_real_estate==1||values.type_real_estate==4||values.type_real_estate==5||values.type_real_estate==6))||values.prodazh==false} >
                             <TextField 
                               variant="outlined"
                               label="Площа, житлова"
                               min={0}
                               step={0.01}
                               display="inline"
                               error={touched.ploshakorysna && Boolean(errors.ploshakorysna)}
                               type="number" 
                               name="ploshakorysna" 
                               id="ploshakorysna" 
                               margin={"dense"}
                               value={this.state.ploshakorysna}
                               onChange={handleChangePloshaKorysna}
                               onKeyDown={handleKeyDown}
                               
                             />
                             </FormControl>
                             <FormControl hidden={(values.prodazh==true&&(values.type_real_estate==1||values.type_real_estate==4||values.type_real_estate==5||values.type_real_estate==6))||values.prodazh==false}>
                             <TextField 
                               variant="outlined"
                               label="Площа, кухня"
                               min={0}
                               step={0.01}
                               display="inline"
                               error={touched.ploshakuchnia && Boolean(errors.ploshakuchnia)}
                               type="number" 
                               name="ploshakuchnia" 
                               id="ploshakuchnia" 
                               margin={"dense"}
                               value={this.state.ploshakuchnia}
                               onChange={handleChangePloshaKuchnia}
                               onKeyDown={handleKeyDown}
                               
                             />
                             </FormControl>

                             <FormControl hidden={values.type_real_estate!==5}>
                             <TextField 
                               variant="outlined"
                               label="Площа ділянки, сот"
                               min={0.01}
                               step={0.01}
                               display="inline"
                               error={touched.ploshadilianku && Boolean(errors.ploshadilianku)}
                               type="number" 
                               name="ploshadilianku" 
                               id="ploshadilianku" 
                               margin={"dense"}
                               value={this.state.ploshadilianku}
                               onChange={handleChangePloshaDilianku}
                               onKeyDown={handleKeyDown}
                               
                             />
                             </FormControl>
                      
                         </FormGroup>    
                         <FormGroup>
                          <FormControl hidden={values.type_real_estate==1||values.type_real_estate==3||values.type_real_estate==5||values.type_real_estate==6}> 
                          <TextField 
                               variant="outlined"
                               label="Поверх"
                               min={0}
                               step={1}
                               display="inline"
                               error={touched.poverx && Boolean(errors.poverx)}
                               type="number" 
                               name="poverx" 
                               id="poverx" 
                               margin={"dense"}
                               
                               onChange={handleChange}
                               onKeyDown={handleKeyDownPoverx}
                             />
                          </FormControl>

                          <FormControl hidden={values.type_real_estate==1||values.type_real_estate==3||values.type_real_estate==5||values.type_real_estate==6}>
                          <TextField 
                               variant="outlined"
                               label="Поверховість"
                               min={0}
                               step={1}
                               display="inline"
                               error={touched.poverxovist && Boolean(errors.poverxovist)}
                               type="number" 
                               name="poverxovist" 
                               id="poverxovist" 
                               margin={"dense"}
                               
                               onChange={handleChange}
                               onKeyDown={handleKeyDownPoverx}
                             />
                          </FormControl>
                         </FormGroup>

                         <FormGroup>
                         <FormControl hidden={values.type_real_estate==1||values.type_real_estate==5||values.type_real_estate==6}>
                          <TextField 
                               variant="outlined"
                               label="К-сть санвузлів"
                               min={0}
                               step={1}
                               display="inline"
                               error={touched.kstsanvusliv && Boolean(errors.kstsanvusliv)}
                               type="number" 
                               name="kstsanvusliv" 
                               id="kstsanvusliv" 
                               margin={"dense"}
                               onChange={handleChange}
                               onKeyDown={handleKeyDownPoverx}
                             />
                          </FormControl>
                         </FormGroup>

                         <FormGroup>
                         <FormControl hidden={values.type_real_estate!==3}>
                          <TextField 
                               variant="outlined"
                               label="К-сть рівнів"
                               min={1}
                               step={1}
                               display="inline"
                               error={touched.kstrivniv && Boolean(errors.kstrivniv)}
                               type="number" 
                               name="kstrivniv" 
                               id="kstrivniv" 
                               margin={"dense"}
                               onChange={handleChange}
                               onKeyDown={handleKeyDown}
                             />
                          </FormControl>
                         </FormGroup>

                         <FormGroup>
                         <FormControl hidden={values.type_real_estate==1||values.type_real_estate==5||values.type_real_estate==6||values.type_real_estate==''}>
                                <TextField variant="outlined"
                                    style={{marginBottom:"7px"}}
                                    select
                                    error={touched.stan && Boolean(errors.stan)}
                                    label="Стан"
                                    name="stan"
                                    id="stan"
                          
                                    margin={"dense"}
                                    onChange={(e)=>{handleChange(e);
          
                                    }}

                                    placeholder="Стан"
                                    >


                                    <MenuItem value={1}>без оздоблення</MenuItem>
                                    <MenuItem value={2}>середній</MenuItem>
                                    <MenuItem value={3}>відмінний</MenuItem>
                                    <MenuItem value={4}>новий ремонт</MenuItem>
                                    
                                </TextField>
                           </FormControl>
                         </FormGroup>
                        <FormGroup>
                          <FormControl hidden={values.type_real_estate==1||values.type_real_estate==5||values.type_real_estate==6||values.type_real_estate==''}>
                            <MultiSelectDropdown name="opalennia" choices={opalenniachoices} labeltext={"Опалення"} onSelectionChange={handleOpalenniaSelectionChange}>
                              </MultiSelectDropdown>
                          </FormControl>
                        </FormGroup>

                         <FormGroup>
                         <FormControl hidden={values.type_real_estate!==2}>
                                <TextField  required variant="outlined"
                                    style={{marginBottom:"7px"}}
                                    select
                                    error={touched.materialstin && Boolean(errors.materialstin)}
                                    label="Матеріал стін"
                                    name="materialstin"
                                    id="materialstin"
                          
                                    margin={"dense"}
                                    onChange={(e)=>{handleChange(e);
          
                                    }}

                                    placeholder="Виберіть матеріал стін"
                                    >


                                    <MenuItem value={1}>цегла</MenuItem>
                                    <MenuItem value={2}>панель</MenuItem>
                                    <MenuItem value={3}>газоблок</MenuItem>
                                    <MenuItem value={4}>піноблок</MenuItem>
                                    <MenuItem value={5}>дерево</MenuItem>
                                </TextField>
                           </FormControl>
                         </FormGroup>

                         <FormGroup>
                          <FormControl hidden={(values.prodazh==true&&(values.type_real_estate==1||values.type_real_estate==2||values.type_real_estate==6))||values.prodazh==false}>
                            <MultiSelectDropdown name="komunikacii" choices={komunikaciichoices} labeltext={"Комунікації"} onSelectionChange={handleKomunikaciiSelectionChange}>
                              </MultiSelectDropdown>
                          </FormControl>
                        </FormGroup>

                         <FormGroup>
                          <FormControl hidden={values.type_real_estate==1||values.type_real_estate==2||values.type_real_estate==4||values.type_real_estate==6||values.type_real_estate==''||values.prodazh==false}>
                            <MultiSelectDropdown name="doisd" choices={doisdchoices} labeltext={"Доїзд"} onSelectionChange={handleDoisdSelectionChange}>
                              </MultiSelectDropdown>
                          </FormControl>
                        </FormGroup>

                         <FormGroup>
                         <FormControl hidden={(values.prodazh==false&&(values.type_real_estate==1||values.type_real_estate==4||values.type_real_estate==5||values.type_real_estate==6))||values.type_real_estate==''||values.prodazh==true}>
                              <FormControlLabel
                                    control={
                                      <Checkbox name="umebliovano"  value={values.umebliovano}  onClick={(event)=>{ setFieldValue("umebliovano",Boolean(event.target.checked));}}/>
                                    }
                                    label="Умебльовано"
                              />
                          </FormControl>
                        </FormGroup>
                        <FormGroup>
                         <FormControl hidden={(values.prodazh==false&&(values.type_real_estate==1||values.type_real_estate==4||values.type_real_estate==5||values.type_real_estate==6))||values.type_real_estate==''||values.prodazh==true}>
                              <FormControlLabel
                                    control={
                                      <Checkbox name="technika"  value={values.technika}  onClick={(event)=>{ setFieldValue("technika",Boolean(event.target.checked));}}/>
                                    }
                                    label="Техніка"
                              />
                          </FormControl>
                        </FormGroup>
                        <ExpansionPanel expanded={this.state.avtomiscepanel=== true} onChange={(e,expanded)=>{handleChange(e,expanded); this.setState({avtomiscepanel:expanded}); }} style={{padding:"5px",backgroundColor:"#eeeeee"}} >
                          <ExpansionPanelSummary
                          expandIcon={<ExpandMoreIcon />}
                          aria-controls="Avtomiscepanel-content"
                          id="Avtomiscepanel"
                          >
                          <Typography>Автомісце</Typography>
                        </ExpansionPanelSummary>

                        <FormGroup>
                          <FormControl>
                                <TextField variant="outlined"
                                  style={{marginBottom:"7px"}}
                                  select
                                  error={touched.avtomiscetype && Boolean(errors.avtomiscetype)}
                                  label="Тип паркінгу"
                                  name="avtomiscetype"
                                  id="avtomiscetype"
                                  value={values.avtomiscetype}
                                  margin={"dense"}
                                  onChange={(e)=>{handleChange(e);
                                  
                                  }}

                                  placeholder="Тип паркінгу"
                                  >
                                  <MenuItem value={1}>Гараж</MenuItem>
                                  <MenuItem value={2}>Відкритий</MenuItem>
                                  <MenuItem value={3}>Закритий</MenuItem>
                              </TextField>
                          </FormControl>

                        
                        


 
                        </FormGroup>
                       
                       </ExpansionPanel>
                       <Grid container alignItems={"flex-end"} >
                           <Grid item md={5} >
                           <FormControl>
                    
                              <TextField variant="outlined"
                                  label="Ціна"
                                  display="inline"
                                  error={touched.cina && Boolean(errors.cina)}

                                  type="number"
                                  name="cina" 
                                  id="cina" 
                                  style = {{marginRight: "15px"}}
                                  inputProps={{ min: "1", max: "999999999", step: "1" }}
                                  pattern='[0-9]{4}'
                                  onKeyDown={e => {
                                    if(values.cina.length>4) return e.preventDefault();
                                    if(e.key=="+") return e.preventDefault();
                                    if(e.key=="-") return e.preventDefault();
                                    if(e.key=="Enter") return e.preventDefault();
                                    if(e.key=="e") return e.preventDefault();
                                    if(e.key=="m") return e.preventDefault();
                                    if(e.key==".") return e.preventDefault();
                                    if(e.key==",") return e.preventDefault();
                                  }}
                                  margin={"dense"}
                                  value={values.cina}
                                  onChange={(e,v)=>  { if(e.target.value.length<=9){if(e.target.value!="0")handleChange(e,v);}}} 
                                  onBlur={handleBlur}
                              />
                           
                            </FormControl>
                          </Grid>
                          <Grid item  md={3} >
                          <FormControl >
                            <TextField variant="outlined"
                                display="inline"
                                select
                                label="Вал"
                                error={touched.valuta && Boolean(errors.valuta)}
                                name="valuta"
                                id="valuta"
                                value={values.valuta}
                                onChange={handleChange}
                                style = {{marginRight: "15px",width:"80px"}}
                                placeholder="Виберіть валюту"
                                margin={"dense"}
                                >

                                <MenuItem value={1}>$</MenuItem>
                                <MenuItem value={2}>€</MenuItem>
                                <MenuItem value={3}>₴</MenuItem>
                            </TextField>
                            </FormControl>
                          </Grid>
                          <Grid item md={4} >
                            <FormControl fullWidth>
                              <TextField variant="outlined"
                                label="Одиниці"
                                select
                                fullWidth
                                display="inline"
                                error={touched.odynuci && Boolean(errors.odynuci)}
                                name="odynuci"
                                id="odynuci"
                                value={values.odynuci}
                                onChange={handleChange}
                                placeholder="Виберіть валюту"
                                margin={"dense"}
                                >

                                <MenuItem value={1}>За об'єкт</MenuItem>
                                <MenuItem value={2} hidden={this.state.objectneruxomosti===false}>за кв.м</MenuItem>
                                <MenuItem value={3} hidden={this.state.objectneruxomosti===true}>за сотку</MenuItem>
                                <MenuItem value={4} hidden={values.prodazh==true}>за місяць</MenuItem>
                                
                              </TextField>
                             </FormControl>
                           </Grid>
                       </Grid>
       <Grid container spacing={4}  hidden={(values.prodazh!==false&&this.state.type===1)||this.state.type==''}>
                          <Grid item container  md={12} >
                            <TextField variant="outlined"
                                select
                                label="Умови співпраці"
                                error={touched.vidnosyny && Boolean(errors.vidnosyny)}
                                name="vidnosyny"
                                id="vidnosyny"
                                fullWidth
                                value={values.vidnosyny}
         
                                margin={"dense"}
                                  onChange= {(e)  =>{
                                    handleChange(e);
                                    const idvidnosyn = e.target.value;
                                    if(idvidnosyn==1)
                                    {
                                    document.getElementById("dilusia_id").style.display="block";
                                    document.getElementById("beru_id").style.display="none";
                                    values.dilusia_hidden= false;
                                    values.beru_hidden = true;
                                    }
                              
                                    if(idvidnosyn==2)
                                    {
                                      document.getElementById("dilusia_id").style.display="none";
                                      document.getElementById("beru_id").style.display="none";
                                      
                                    values.dilusia_hidden= true;
                                    values.beru_hidden = true;

                                    
                                    }
                                    if(idvidnosyn==3)
                                    {
                                      document.getElementById("dilusia_id").style.display="none";
                                      document.getElementById("beru_id").style.display="block";

                                    values.dilusia_hidden= true;
                                    values.beru_hidden = false;
                                    
                                    }
                              }
                              }
                                >
                                <MenuItem value={1}  onChange={handleChange}>ділюся % від власника</MenuItem>
                                <MenuItem value={2}  onChange={handleChange}>на % від покупця не претендую</MenuItem>
                                <MenuItem value={3}  onChange={handleChange}>хочу % від покупця</MenuItem>
                            </TextField>
                            </Grid>
                        </Grid>
                        <Box component="div" id="dilusia_id" display="none" style={{marginTop:"15px",marginBottom:"15px"}} hidden={(values.prodazh!==false&&this.state.type===1)||this.state.type==''}>
                            <label display="inline"  style={{marginRight:"15px",marginLeft:"15px"}}>Ділюся</label> 
                            <Select variant="outlined"
                                display="inline"
                                error={touched.dilusia && Boolean(errors.dilusia)}
                                name="dilusia"
                                id="dilusia"
                                value={values.dilusia}
                                onChange={(e)  =>{
                                  handleChange(e);
                                  const dl = e.target.value;
                                  this.setState({dilusiaselect:dl});
                                }}
                                placeholder="Виберіть ділюся"
                                style={{marginRight:"15px"}}
                                >
                                <MenuItem value={1}>%</MenuItem>
                                <MenuItem value={2}>$</MenuItem>
                                <MenuItem value={3}>€</MenuItem>
                                <MenuItem value={4}>₴</MenuItem>
                            </Select>

                              <TextField
                                  variant="outlined"
                                  label={this.state.dilusiaselect==1 ? "Комісія" : "Сума"}
                                  display="inline"
                                  error={touched.komisija && Boolean(errors.komisija)}
                                  type="number" 
                                  name="komisija" 
                                  id="komisija" 
                                  min={0}
                                  max={10}
                                  value={values.komisija}
                                  onChange={handleChange}
                                  onBlur={handleBlur}
                                  
                                  style={{width:"120px"}}
                                  
                                />
                          
                        </Box>
                        <Box component="div"  id="beru_id" display="none" style={{marginTop:"15px",marginBottom:"15px"}} hidden={(values.prodazh!==false&&this.state.type===1)||this.state.type==''}>
                          <label  display="inline"  style={{marginRight:"15px",marginLeft:"15px"}}>Беру&nbsp;&nbsp;</label> 
                          <Select variant="outlined"
                                display="inline"
                                error={touched.beru && Boolean(errors.beru)}
                                name="beru"
                                id="beru"
                                value={values.beru}
                                style={{marginRight:"15px"}}
                                onChange={(e)  =>{
                                  handleChange(e);
                                  const dls = e.target.value;
                                  this.setState({beruselect:dls});
                                }}
                                >
                                <MenuItem value={1}>%</MenuItem>
                                <MenuItem value={2}>$</MenuItem>
                                <MenuItem value={3}>€</MenuItem>
                                <MenuItem value={4}>₴</MenuItem>
                            </Select>
                                <TextField variant="outlined"
                                  label={this.state.beruselect==1 ? "Комісія" : "Сума"}
                                  display="inline"
                                  error={touched.komisija_beru && Boolean(errors.komisija_beru)}
                                  type="text" 
                                  name="komisija_beru" 
                                  id="komisija_beru" 
                                  style={{width:"120px"}}
                                  value={values.komisija_beru} 
                                  onChange={handleChange} 
                                  onBlur={handleBlur}
                              />

                        </Box>
                        <FormGroup>
                        <FormControl>
                            <TextField hidden={(values.prodazh!==false&&this.state.type===1)||values.prodazh===false&&this.state.type!==1||this.state.type==''}
                                variant="outlined" required
                                display="inline"
                                select
                                label="Умови продажу"
                                error={touched.umovuprodazhy && Boolean(errors.umovuprodazhy)}
                                name="umovuprodazhy"
                                id="umovuprodazhy"
                                value={values.umovuprodazhy}
                                onChange={handleChange}
                                placeholder="Виберіть умову"
                                margin={"dense"}
                                >

                                <MenuItem value={1}>Чистий продаж</MenuItem>
                                <MenuItem value={2}>Заміна</MenuItem>
                                <MenuItem value={3}>Іпотека</MenuItem>
                            </TextField>
                          </FormControl>
                        </FormGroup>

                        <FormGroup>
                          <FormControl hidden={values.prodazh!==false}>
                            <TextField variant="outlined" required
                                display="inline"
                                select
                                label="Термін оренди"
                                error={touched.terminorendu && Boolean(errors.terminorendu)}
                                name="terminorendu"
                                id="terminorendu"
                                value={values.terminorendu}
                                onChange={handleChange}
                                placeholder="виберіть термін"
                                margin={"dense"}
                                >

                                <MenuItem value={1}>до 3-х місяців</MenuItem>
                                <MenuItem value={2}>від 3-х до 6 місяців</MenuItem>
                                <MenuItem value={3}>від 6 місяців</MenuItem>
                            </TextField>
                          </FormControl>
                          <FormControl hidden={true}>
                                <FormControlLabel
                                      control={
                                        <Checkbox name="juridichnagotovnist"  value={values.juridichnagotovnist}  error={errors.juridichnagotovnist} onClick={(event)=>{ setFieldValue("juridichnagotovnist",Boolean(event.target.checked));}}/>
                                      }
                                      label="Юридична готовність *"
                                    />
                          </FormControl>
                          <FormControl  hidden={true}>
                                <FormControlLabel
                                      control={
                                        <Checkbox name="podatokzprodazhu"  value={values.podatokzprodazhu}  onClick={(event)=>{ setFieldValue("podatokzprodazhu",Boolean(event.target.checked));}}/>
                                      }
                                      label="Податок з продажу"
                                    />
                          </FormControl>
                          <FormControl  hidden={true}>
                            <TextField variant="outlined"
                                    select
                                    label="Власник"
                                    display="inline"
                                    error={touched.osoba && Boolean(errors.osoba)}
                                    name="osoba"
                                    id="osoba"
                                    value={values.osoba}
                                    onChange={handleChange}
                                    margin={"dense"}
                                    >
                                    <MenuItem value={1}>Фізична особа</MenuItem>
                                    <MenuItem value={2}>Юридична особа</MenuItem>
                            </TextField>
                          </FormControl>

                          <FormControl>
                              <TextField 
                                variant="outlined"
                                label="Опис"
                                error={touched.dodatkovoproon && Boolean(errors.dodatkovoproon)}
                                name="dodatkovoproon" 
                                id="dodatkovoproon" 
                                value={values.dodatkovoproon}
                                onChange={handleChange}
                                margin={"dense"}
                                multiline
                                rows={5}
                                inputProps={
                                  {maxLength:500}
                                }
                              />
                          </FormControl>
                        </FormGroup>
                        <FormControl  hidden={true}>
                            <FormControlLabel
                                  control={
                                    <Checkbox name="podatynaportal" defaultChecked value={values.podatynaportal}  onClick={(event)=>{ setFieldValue("podatynaportal",Boolean(event.target.checked));}}/>
                                  }

                                  label="Подати на портал"
                                />
                        </FormControl>
                        <ImagesUploadDraggable display={true} setState={this.setParentState.bind(this)} imgcount={20} statename={"imgs"} caption={"Фото ОН"}/>
                        <FormGroup>
                          <Button variant="contained"  type="submit" disabled={isSubmitting} 
                          style=
                          {{backgroundColor:outerTheme.palette.primary.light, color:"white"}}>
                                  Додати
                          </Button>
                        </FormGroup>
                   </form>  
                   )
                }
                 
             </Formik>
                 </Container>
                   </ThemeProvider>
        );
    }
};

if (document.getElementById('onform')) {
    ReactDOM.render(<OnForm />, document.getElementById('onform'));
}

