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
import LocationFields from './LocationFields';
import BudivliaFields from './BudivliaFields';
import TexxarakterFields from './TexxarakterFields';
import DiliankaFields from "./DiliankaFields";
import KomunikaciiFields from "./KomunikaciiFields";
import ImagesUploadDraggable from "./ImagesUploadDraggable";
import Mapp from "./Mapp";
const validationSchema = Yup.object().shape({
    vysotasteli: Yup.number().moreThan(0),  
    prodazh: Yup.bool().required(),
    vydvukorystannia:Yup.number().moreThan(0).when('type_real_estate',{
      is: 4,
      then: fieldSchema => fieldSchema.required(),
    }),
    juridichnagotovnist: Yup.bool().required(),
    type_real_estate: Yup.number().moreThan(0).required("Виберіть тип нерухомості"),
    kadastrovyi:Yup.string().
     when('type_real_estate',{
      is: 3,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 5,
      then: fieldSchema => fieldSchema.required(),
    }),
    korystuvannia:Yup.number().moreThan(0).
     when('type_real_estate',{
      is: 3,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 5,
      then: fieldSchema => fieldSchema.required(),
    }),
    area_earth:Yup.number().moreThan(0).
     when('type_real_estate',{
      is: 3,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 5,
      then: fieldSchema => fieldSchema.required(),
    }),
    budynoktype: Yup.number().moreThan(0).
     when('type_real_estate',{
      is: 3,
      then: fieldSchema => fieldSchema.required(),
    }),
    budivliatype: Yup.number().moreThan(0).
     when('type_real_estate',{
      is: 1,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 2,
      then: fieldSchema => fieldSchema.required(),
    }),
     poverx: Yup.number().moreThan(0).
     when('type_real_estate',{
      is: 1,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 2,
      then: fieldSchema => fieldSchema.required(),
    }),
    kstpoverxiv: Yup.number().moreThan(0).
     when('type_real_estate',{
      is: 1,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 2,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 3,
      then: fieldSchema => fieldSchema.required(),
    }),
    matstin: Yup.number().moreThan(0).
     when('type_real_estate',{
      is: 1,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 2,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 3,
      then: fieldSchema => fieldSchema.required(),
    }),
    kstspalen: Yup.number().moreThan(0).
     when('type_real_estate',{
      is: 2,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 3,
      then: fieldSchema => fieldSchema.required(),
    }),
    kstsanvuzliv: Yup.number().moreThan(0).
     when('type_real_estate',{
      is: 2,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 3,
      then: fieldSchema => fieldSchema.required(),
    }),
     vilneplanuvannia: Yup.bool().
     when('type_real_estate',{
      is: 2,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 3,
      then: fieldSchema => fieldSchema.required(),
    }),
      opalennia: Yup.number().moreThan(0).
     when('type_real_estate',{
      is: 1,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 2,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 3,
      then: fieldSchema => fieldSchema.required(),
    }),
    stankim: Yup.number().moreThan(0).
     when('type_real_estate',{
      is: 1,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 2,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 3,
      then: fieldSchema => fieldSchema.required(),
    }),
    naspunkt: Yup.string().when('type_real_estate',{
      is: 1,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 2,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 3,
      then: fieldSchema => fieldSchema.required(),
    }),
    rayon: Yup.string().when('type_real_estate',{
      is: 1,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 2,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 3,
      then: fieldSchema => fieldSchema.required(),
    }),
     vulica: Yup.string().when('type_real_estate',{
      is: 1,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 2,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 3,
      then: fieldSchema => fieldSchema.required(),
    }),
    cina: Yup.string().required("Введіть ціну"),
    valuta: Yup.number().required(),
    odynuci: Yup.number().required(),
    vidnosyny: Yup.number().moreThan(0).required("Вкажіть відносини"),
    komisija: Yup.string().when('vidnosyny', {
        is: 1,
        then: fieldSchema => fieldSchema.required(),
    }),
    komisija_beru: Yup.string().when('vidnosyny',{
      is: 3,
      then: fieldSchema => fieldSchema.required(),
    }),
    zagplosha: Yup.number().moreThan(0)
    .when('type_real_estate',{
      is: 1,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 2,
      then: fieldSchema => fieldSchema.required(),
    }).when('type_real_estate',{
      is: 3,
      then: fieldSchema => fieldSchema.required(),
    })
    

});

  //const filteredOptions = options2.filter((o) => o.link === this.state.selectedOption.value)

export default class DependingForm extends Component {
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
    }
   
  }
 
  async componentDidMount() {
   // nevtags, additionalnevtags, zk, zabudovnuk
    let [naspunkti, vul, rayons,] = await Promise.all([
      await Axios.get('/getnaspunkt.json'),
      await Axios.get('/getvulyci.json'), 
      await Axios.get('/getrayonu.json'),
      // await Axios.get('/getnevtags.json'),
      // await Axios.get('/getadditionalnevtags.json'),
      // await Axios.get('/getzk.json'),
      // await Axios.get('/getzabudovnuk.json'),
      
    ]);
    console.log(vul.data);
    if(naspunkti.status == 200){
     this.setState({naspunkts:naspunkti.data});
    }
    if(vul.status == 200){
    
      this.setState({vulyci:vul.data});
    }
    if(rayons.status == 200){
      this.setState({rayon:rayons.data});
    }
    console.log(this.state.naspunkts);
    console.log(this.state.vulyci);
    console.log(this.state.rayon);
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

        const filteredOptions = options2.filter((o) => o.misto === this.state.selectedOption);
        const filteredOptions2 = options3.filter((o) => o.link === this.state.selectedOption);
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
        return (
          
        <ThemeProvider theme={themecustom}>
        
         <Container style={{widht:"100%",height:"100%"}}>
            <Formik  
            
                initialValues={{
                 prodazh:true,type_real_estate: '', naspunkt: '', cina:'',
                 valuta:1, odynuci:1, vidnosyny: '',
                 komisija:'', osoba:1, dilusia:1, oblast: 0,
                 komisija_beru:'',beru:1,beru_hidden:true, dilusia_hidden:true,
                 rayon:'', vulica: '',budynok :'',kvartyra:'',korpus: '',kadastrovyi:'',lat:'',lng:'',svitlo:false,gaz:false,
                 budivliatype:'',korystuvannia:'',pryznachennia:'',voda:'',kanalizacia:'',kstpoverxiv:'',matstin:'',
                 matperekrytya:'',matsxodiv:'',pamyatkarx:'',databudivnyctva:null,probudivliu:'',zakrytateritoria:false,
                 klasbudivli:'',kadastrovyi_budivlia:'',planuvannia_budynku:'',stanbudivnuctva:'',zagplosha:'',korysnaplosha:'',
                 kuchniplosha:'',dush:false,vanna:false,tualet:false,poverx:'',kimnatade:'',opalennia:'',stankim:'',vxid:'',vxidv:'',
                 kstbalkoniv:'',kstrivniv:1,kstsanvuzliv:'',vilneplanuvannia:false,kstspalen:'',vydvukorystannia:'',kstvitryn:'',
                 kstrivnivmisce:1,avtomiscetype:'',poverxmisce1:'',matavtomisce:'',parkovkanavulyci:'',stanavtomisce:'',
                 remontstyle:'',landshaftnuidesign:false,remontstyletags:'',budynoktype:'',kstrivnivbudynok:'',zdachiakvartal:'',dojizd:'',
                 kstbalkonivextended:'',chergabudivnyctva:'',umovuprodazhy:'',juridichnagotovnist:false,podatokzprodazhu:false,dodatkovoproon:'',
                 podatynaportal:true,potyzhnist:'',vxidvprymishennia:[],parkomisc:'',vysotasteli:'',area_earth:''
                 
                }}
                validationSchema={validationSchema}
                onSubmit = {(values, { setSubmitting, resetForm, setValues }) => {


                 setSubmitting(true);
                    
                     setTimeout(async () => {
                        alert(JSON.stringify(values,null,2));
                        console.log(JSON.stringify(values,null,2));
                        //setFieldValue("onimages",this.state.imgs);

                      var imgs = this.state.imgs;
                      let array1= await Promise.all(imgs.map(async (element)=> {
                            const imgheader = {
                                data : element,
                                dir : 'on'
                            };
                            return axios.post('makeimage',imgheader).then((response)=> {
                              return response.data.id;
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
                                          "onimages":  this.state.imgsback,
                                          "photobud":  this.state.photobudback,  
                                          "photoplanuvannia":  this.state.photoplanuvanniaback,
                                          "photozemlia":  this.state.photozemliaback,
                                          "currentPos": this.state.currentPos
                                         } 

                        await setValues(payload);
                        await axios.post('objectneruxomosti',payload).then(function (response) {
                          console.log(response);
                          resetForm();
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
      
                      {//JSON.stringify(errors)
                      }
                        <FormGroup style={{display: 'flex', alignItems: 'center', justifyContent: 'center',}} >
                          <FormControl component="fieldset" >
      
                            <RadioGroup value={values.prodazh} name="prodazh" row>
                                <FormControlLabel

                                value={true}
                                control={<Radio style ={{
                                  color: outerTheme.palette.primary.light,
                                }} />}
                                label="Продаж"
                                labelPlacement="end"
                                onChange={() => setFieldValue("prodazh", true) }

                                />
                                <FormControlLabel
                                value={false}
                                control={<Radio style ={{
                                  color: outerTheme.palette.primary.light,
                                }} />}
                                label="Оренда"
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
                                <MenuItem value={6}>Автомісце</MenuItem>
                            </TextField>
                            
                        </FormControl>
                       </FormGroup>
                          <FormGroup hidden={values.type_real_estate!==4}>
                         <FormControl hidden={values.type_real_estate!==4}>
                              <TextField variant="outlined"
                                style={{marginBottom:"7px"}}
                                select
                                error={touched.vydvukorystannia && Boolean(errors.vydvukorystannia)}
                                label="Вид використання"
                                name="vydvukorystannia"
                                id="vydvukorystannia"
                                value={values.vydvukorystannia}
                                margin={"dense"}
                                onChange={(e)=>{handleChange(e);
                                 
                                }}

                                placeholder="Виберіть вид використання"
                                >
                                <MenuItem value={1}>офіс</MenuItem>
                                <MenuItem value={2}>торгівля</MenuItem>
                                <MenuItem value={3}>громадське харчування</MenuItem>
                                <MenuItem value={4}>склад</MenuItem>
                                <MenuItem value={5}>виробництво</MenuItem>
                                <MenuItem value={6}>готовий бізнес</MenuItem>
                                <MenuItem value={7}>інше</MenuItem>
                            </TextField>
                       </FormControl>
                       <FormControl hidden={values.vydvukorystannia!==6}>
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
                              setFieldValue("nev",v);
                                           
                            }}
                            >
                        
                          </Autocomplete>
                          
                       </FormControl>

                       <FormControl hidden={values.vydvukorystannia!==7}>
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
                        <FormControl  hidden={values.vydvukorystannia!==6&&values.vydvukorystannia!==2}>
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
                      <FormGroup hidden={values.vydvukorystannia!==4&&values.vydvukorystannia!==5}>
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
                       <LocationFields setState={this.setParentState.bind(this)} state={this.state} handleChange={handleChange} handleBlur={handleBlur} values={values} touched={touched} errors={errors}
                          options1={options1}  options2={options2} options3={options3} filteredOptions={filteredOptions} filteredOptions2={filteredOptions2} setFieldValue={setFieldValue}
                          display={this.state.type==1||this.state.type==2||this.state.type==3||this.state.type==4}
                       />
                        <FormGroup>
                        <FormControl hidden={Boolean(values.type_real_estate!=4)}>
                              <FormControlLabel
                                    control={
                                      <Checkbox name="okremostojachyi"  value={values.okremostojachyi}  onClick={(event)=>{ setFieldValue("okremostojachyi",Boolean(event.target.checked));}}/>
                                    }
                                    label="Окремостоячий"
                              />
                          </FormControl>
                        </FormGroup>
                    
                      
                      
                       <DiliankaFields setState={this.setParentState.bind(this)} state={this.state} handleChange={handleChange} handleBlur={handleBlur} values={values} touched={touched} errors={errors}
                           setFieldValue={setFieldValue}
                          display={this.state.type==3||this.state.type==5||values.okremostojachyi}
                       />

                        <KomunikaciiFields setState={this.setParentState.bind(this)} state={this.state} handleChange={handleChange} handleBlur={handleBlur} values={values} touched={touched} errors={errors}
                           setFieldValue={setFieldValue}
                          display={this.state.type==3||this.state.type==4||this.state.type==5}
                       />
            
                        <BudivliaFields setState={this.setParentState.bind(this)} state={this.state} handleChange={handleChange} handleBlur={handleBlur} values={values} touched={touched} errors={errors}
                          kistpoverxiv={kistpoverxiv} setFieldValue={setFieldValue} zabudovnukoptions={zabudovnukoptions} zkoptions={zkoptions}
                          display={this.state.type==1||this.state.type==2||this.state.type==3||this.state.type==4}
                       />
               
                       <FormGroup>
                      
                          <TextField 
                            variant="outlined"
                            margin="dense"
                            name="lat"
                            id="lat"
                            value={this.state.currentPos ? this.state.currentPos.lat :''}
                              onChange={(e)=>{handleChange(e);
                                  
                                  }}
                    
                          >
                          </TextField>

                          <TextField 
                            variant="outlined"
                            margin="dense"
                            name="lng"
                            id="lng"
                            value={this.state.currentPos ? this.state.currentPos.lng :''}
                            onChange={(e)=>{handleChange(e);
                                  
                                  }}
                          >
                          </TextField>
                       
                       </FormGroup>
                      <TexxarakterFields setState={this.setParentState.bind(this)} state={this.state} handleChange={handleChange} handleBlur={handleBlur} values={values} touched={touched} errors={errors}
                          kistpoverxiv={kistpoverxiv} setFieldValue={setFieldValue} countries={countries} poverxy={poverxy}
                          display={this.state.type==1||this.state.type==2||this.state.type==3||this.state.type==4}
                       />
                        
                               
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
                                  label="Тип автомісця"
                                  name="avtomiscetype"
                                  id="avtomiscetype"
                                  value={values.avtomiscetype}
                                  margin={"dense"}
                                  onChange={(e)=>{handleChange(e);
                                  
                                  }}

                                  placeholder="Тип автомісця"
                                  >
                                  <MenuItem value={1}>Гараж в будинку</MenuItem>
                                  <MenuItem value={2}>Гараж окремостоячий</MenuItem>
                                  <MenuItem value={3}>Паркомісце закрите</MenuItem>
                                  <MenuItem value={4}>Паркомісце на вулиці</MenuItem>
                              </TextField>
                          </FormControl>
                          <FormControl hidden={values.avtomiscetype!==1}>
                            <TextField 
                              variant="outlined"
                              label="Адреса будинку"
                              display="inline"
                              error={touched.adresabudynku && Boolean(errors.adresabudynku)}
                              type="text" 
                              name="adresabudynku" 
                              id="adresabudynku" 
                               margin={"dense"}
                              
                            />
                        </FormControl>
                        <FormControl hidden={values.avtomiscetype!=2 && values.avtomiscetype!=3}>
                            <TextField 
                              variant="outlined"
                              label="Адреса"
                              display="inline"
                              error={touched.adresaavtomisce && Boolean(errors.adresaavtomisce)}
                              type="text" 
                              name="adresaavtomisce" 
                              id="adresaavtomisce" 
                               margin={"dense"}
                              
                            />
                        </FormControl>
                        <FormControl hidden={values.avtomiscetype!=1 && values.avtomiscetype!=2 && values.avtomiscetype!=3}>
                         <TextField
                             variant="outlined"
                             label="Опис місця"
                             display="inline"
                             error={touched.opys_misca && Boolean(errors.opys_misca)}
                             type="text" 
                             name="opys_misca" 
                             id="opys_misca" 
                              multiline   
                              margin={"dense"}
                             
                           />
                        </FormControl>
                        <FormControl hidden={values.avtomiscetype!=1 && values.avtomiscetype!=2 && values.avtomiscetype!=3}>
                            <TextField 
                              variant="outlined"
                              label="Площа, загальна"
                              display="inline"
                              error={touched.ploshamisca && Boolean(errors.ploshamisca)}
                              type="number" 
                              name="ploshamisca" 
                              id="ploshamisca" 
                               margin={"dense"}
                              
                            />
                        </FormControl>
                        
                         <FormControl hidden={values.avtomiscetype!==2}>
                                <TextField  required variant="outlined"
                                    style={{marginBottom:"7px"}}
                                    select
                                    error={touched.matavtomisce && Boolean(errors.matavtomisce)}
                                    label="Матеріал стін"
                                    name="matavtomisce"
                                    id="matavtomisce"
                                    value={values.matavtomisce}
                                    margin={"dense"}
                                    onChange={(e)=>{handleChange(e);
          
                                    }}

                                    placeholder="Виберіть матеріал стін"
                                    >


                                    <MenuItem value={1}>цегла</MenuItem>
                                    <MenuItem value={2}>панель</MenuItem>
                                    <MenuItem value={3}>газоблок</MenuItem>
                                    <MenuItem value={4}>піноблок</MenuItem>
                                    <MenuItem value={5}>метал</MenuItem>
                                    <MenuItem value={6}>дерево</MenuItem>
                                </TextField>
                           </FormControl>
                           <FormControl hidden={values.avtomiscetype!==2}>
                                <TextField variant="outlined"
                                  style={{marginBottom:"7px"}}
                                  select
                                  error={touched.kstrivnivmisce && Boolean(errors.kstrivnivmisce)}
                                  label="Кількість рівнів"
                                  name="kstrivnivmisce"
                                  id="kstrivnivmisce"
                                  value={values.kstrivnivmisce}
                                  margin={"dense"}
                                  onChange={(e)=>{handleChange(e);
                                    setFieldValue("kstrivnivmisce",e.target.value);
                                  }}

                                  placeholder="Виберіть кількість рівнів"
                                  >
                                  <MenuItem value={1}>1</MenuItem>
                                  <MenuItem value={2}>2</MenuItem>
                                  <MenuItem value={3}>3</MenuItem>
                                  <MenuItem value={4}>4</MenuItem>
                              </TextField>
                            </FormControl>
                            <FormControl  hidden={values.avtomiscetype!==2}>
                                <TextField variant="outlined"
                                    style={{marginBottom:"7px"}}
                                    select
                                    error={touched.poverxmisce1 && Boolean(errors.poverxmisce1)}
                                    label="Поверх"
                                    name="poverxmisce1"
                                    id="poverxmisce1"
                                    value={values.poverxmisce1}
                                    margin={"dense"}
                                    onChange={(e)=>{handleChange(e);
                                    
                                    }}

                                    placeholder="Виберіть поверх"
                                    >


                                            {poverxy.map(option => (
                                            <MenuItem key={option} value={option} >
                                              {option}
                                            </MenuItem>
                                          ))} 
                                </TextField>
                            </FormControl>
                            <FormControl hidden={values.avtomiscetype!=1 && values.avtomiscetype!=2}>
                              <TextField variant="outlined"
                                style={{marginBottom:"7px"}}
                                select
                                error={touched.stanavtomisce && Boolean(errors.stanavtomisce)}
                                label="Стан"
                                name="stanavtomisce"
                                id="stanavtomisce"
                                value={values.stanavtomisce}
                                margin={"dense"}
                                onChange={(e)=>{handleChange(e);
                                 
                                }}

                                placeholder="Виберіть стан"
                                >
                                <MenuItem value={1}>-</MenuItem>
                                <MenuItem value={2}>без оздобення</MenuItem>
                                <MenuItem value={3}>середній</MenuItem>
                                <MenuItem value={4}>відмінний</MenuItem>
                                <MenuItem value={5}>новий ремонт</MenuItem>
                            </TextField>
                         </FormControl>
                            <FormControl hidden={values.avtomiscetype!==4}>
                                <TextField variant="outlined"
                                  style={{marginBottom:"7px"}}
                                  select
                                  error={touched.parkovkanavulyci && Boolean(errors.parkovkanavulyci)}
                                  label="Парковка на вулиці"
                                  name="parkovkanavulyci"
                                  id="parkovkanavulyci"
                                  value={values.parkovkanavulyci}
                                  margin={"dense"}
                                  onChange={(e)=>{handleChange(e);
                                  
                                  }}

                                  placeholder="Парковка на вулиці"
                                  >
                                  <MenuItem value={1}>стихійна</MenuItem>
                                  <MenuItem value={2}>1 місце</MenuItem>
                                  <MenuItem value={3}>2 місця</MenuItem>
                                  <MenuItem value={4}>3+ місця</MenuItem>
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
                        <Grid container spacing={4}  >
                          <Grid item container  md={12} >
                            <TextField variant="outlined"
                                select
                                label="Відносини з власником"
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
                                    console.log("1");
                                    console.log(values.dilusia_hidden);
                                    console.log(values.beru_hidden);

                                    }
                              
                                    if(idvidnosyn==2)
                                    {
                                      document.getElementById("dilusia_id").style.display="none";
                                      document.getElementById("beru_id").style.display="none";
                                      
                                    values.dilusia_hidden= true;
                                    values.beru_hidden = true;

                                    console.log("2");
                                    console.log(values.dilusia_hidden);
                                    console.log(values.beru_hidden);
                                    
                                    }
                                    if(idvidnosyn==3)
                                    {
                                      document.getElementById("dilusia_id").style.display="none";
                                      document.getElementById("beru_id").style.display="block";

                                    values.dilusia_hidden= true;
                                    values.beru_hidden = false;
                                    console.log("3");
                                    console.log(values.dilusia_hidden);
                                    console.log(values.beru_hidden);
                                    }
                              }
                              }
                                >
                                <MenuItem value={1}  onChange={handleChange}>Договір з ділення комісії</MenuItem>
                                <MenuItem value={2}  onChange={handleChange}>На комісію від покупця не претендую</MenuItem>
                                <MenuItem value={3}  onChange={handleChange}>Хочу отримати комісію від покупця</MenuItem>
                            </TextField>
                            </Grid>
                        </Grid>
                        <Box component="div" id="dilusia_id" display="none" style={{marginTop:"15px",marginBottom:"15px"}} >
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
                        <Box component="div"  id="beru_id" display="none" style={{marginTop:"15px",marginBottom:"15px"}} >
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
                          <FormControl >
                            <TextField variant="outlined" required
                                display="inline"
                                select
                                label="Умови продажу"
                                error={touched.umovuprodazhy && Boolean(errors.umovuprodazhy)}
                                name="umovuprodazhy"
                                id="umovuprodazhy"
                                value={values.umovuprodazhy}
                                onChange={handleChange}
                                placeholder="Виберіть валюту"
                                margin={"dense"}
                                >

                                <MenuItem value={1}>Чистий продаж</MenuItem>
                                <MenuItem value={2}>Заміна</MenuItem>
                                <MenuItem value={3}>В іпотеці</MenuItem>
                            </TextField>
                          </FormControl>
                          <FormControl>
                                <FormControlLabel
                                      control={
                                        <Checkbox name="juridichnagotovnist"  value={values.juridichnagotovnist}  error={errors.juridichnagotovnist} onClick={(event)=>{ setFieldValue("juridichnagotovnist",Boolean(event.target.checked));}}/>
                                      }
                                      label="Юридична готовність *"
                                    />
                          </FormControl>
                          <FormControl>
                                <FormControlLabel
                                      control={
                                        <Checkbox name="podatokzprodazhu"  value={values.podatokzprodazhu}  onClick={(event)=>{ setFieldValue("podatokzprodazhu",Boolean(event.target.checked));}}/>
                                      }
                                      label="Податок з продажу"
                                    />
                          </FormControl>
                          <FormControl >
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
                                label="Додатково про ОН"
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
                        <FormControl>
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

if (document.getElementById('dependingform')) {
    ReactDOM.render(<DependingForm />, document.getElementById('dependingform'));
}

