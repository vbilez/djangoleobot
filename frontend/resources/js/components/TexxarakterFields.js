
import React, { Component, RadioButton,Fragment } from 'react';
import {Container, TextField, FormGroup, Button, RadioGroup, Select, 
        MenuItem, Box, FormControl, Radio,FormControlLabel, Grid, Checkbox,InputLabel
} from '@material-ui/core';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Typography from '@material-ui/core/Typography';
import {Autocomplete} from '@material-ui/lab';
import { DatePicker,MuiPickersUtilsProvider } from "@material-ui/pickers";
import DateFnsUtils from '@date-io/date-fns';
import ruLocale from "date-fns/locale/ru";
import PoverxField from "./PoverxField";
import KstrivnivField from "./KstrivnivField";
import VxidFields from "./VxidFields";
import KstspalenField from "./KstspalenField";
import KimnatavkvartyriField from "./KimnatavkvartyriField";
import SanvyzolFields from "./SanvyzolFields";
import KstsanvuzlivField from "./KstsanvuzlivField";
import VilneplanuvanniaField from "./VilneplanuvanniaField";
import Chip from '@material-ui/core/Chip';
 export default class TexxarakterFields extends Component {
   constructor(props) {
    super(props);
   }

        
        render(){
            const ITEM_HEIGHT = 48;
                const ITEM_PADDING_TOP = 8;
                const MenuProps = {
                PaperProps: {
                    style: {
                    maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
                    width: 250,
                    },
                },
                };
          if(this.props.display){
          return (
 <ExpansionPanel expanded={this.props.state.texxarakter=== true} onChange={(e,expanded)=>{ this.props.setState({texxarakter:expanded}); }} style={{padding:"5px",backgroundColor:"#eeeeee"}} >
                          <ExpansionPanelSummary
                          expandIcon={<ExpandMoreIcon />}
                          aria-controls="Texxarakter-content"
                          id="Texxarakter"
                          >
                          <Typography>Технічні характеристики</Typography>
                          </ExpansionPanelSummary>
                       <FormGroup>
                        <PoverxField handleChange={this.props.handleChange} values={this.props.values} touched={this.props.touched} errors={this.props.errors} poverxy={this.props.poverxy} 
                            display={this.props.state.type==1||this.props.state.type==2||this.props.state.type==4}
                        />
                        <KstrivnivField handleChange={this.props.handleChange} values={this.props.values} touched={this.props.touched} errors={this.props.errors} 
                            display={this.props.state.type==3||this.props.state.type==2||this.props.state.type==4}
                        />    
                        <VxidFields handleChange={this.props.handleChange} values={this.props.values} touched={this.props.touched} errors={this.props.errors}  
                            display={this.props.state.type==2}
                        />    
                        <KstspalenField handleChange={this.props.handleChange} values={this.props.values} touched={this.props.touched} errors={this.props.errors}  
                             display={this.props.state.type==3||this.props.state.type==2}
                        />    
                         <KimnatavkvartyriField  values={this.props.values}   setFieldValue={this.props.setFieldValue}
                             display={this.props.state.type==1}
                        />
                      <Grid container >
                        <Grid item md={4} xs={4} sm={4}>
                            <TextField variant="outlined" 
                            label="Площа"
                            error={this.props.touched.zagplosha && Boolean(this.props.errors.zagplosha)}
                            display="inline"
                            type="text" 
                            name="zagplosha" 
                            id="zagplosha" 
                            onBlur={this.props.handleBlur}
                            value={this.props.values.zagplosha}
                            margin={"dense"}

                            style = {{marginRight: "15px"}}
                            inputProps={{
                                maxLength: 6
                            }}
                            onKeyDown={e => {
                                    if(this.props.values.zagplosha.length>6) return e.preventDefault();//dovznyna vvody
                                    if(e.key=="+") return e.preventDefault();
                                    if(e.key=="-") return e.preventDefault();
                                    if(e.key=="Enter") return e.preventDefault();
                                    if(e.key=="e") return e.preventDefault();
                                    if(e.key=="m") return e.preventDefault();
                                    if( e.key=="2" || e.key=="3" || e.key=="4" || e.key=="5" || e.key=="6" || e.key=="7" || e.key=="8" || e.key=="9" || e.key=="1" || e.key=="0") 
                                    {
                                        if(this.props.values.zagplosha.toString().indexOf(".")>-1)
                                        {
                                            let index1 = this.props.values.zagplosha.toString().indexOf(".");
                                            let str1 = this.props.values.zagplosha.toString().slice(index1,this.props.values.zagplosha.toString().length );
                                            if(str1.length>1) return e.preventDefault();//znakiv pislia komu
                                        }
                                     
                                    } 
                                  }}
                            onChange={(e,v)=>  { 
                                if(!Number(e.target.value)&& e.target.value.length>=1 
                                && e.target.value!="1" 
                                && e.target.value!="2"
                                && e.target.value!="3"
                                && e.target.value!="4"
                                && e.target.value!="5"
                                && e.target.value!="6"
                                && e.target.value!="7"
                                && e.target.value!="8"
                                && e.target.value!="9"
                                ) return;
                                 if(e.target.value.length<=6){//dovznyna vvody
                                        if(e.target.value!="0")this.props.handleChange(e,v);
                                    }
                                }}
                            />
                        </Grid>
                            
                        <Grid item md={4}  xs={4} sm={4} >
                            <TextField variant="outlined"
                                label="Житлова"
                                error={this.props.touched.korysnaplosha && Boolean(this.props.errors.korysnaplosha)}
                                display="inline"
                                type="text" 
                                name="korysnaplosha" 
                                id="korysnaplosha" 
                                onKeyDown={e => {
                                    if(this.props.values.korysnaplosha.length>6) return e.preventDefault();//dovznyna vvody
                                    if(e.key=="+") return e.preventDefault();
                                    if(e.key=="-") return e.preventDefault();
                                    if(e.key=="Enter") return e.preventDefault();
                                    if(e.key=="e") return e.preventDefault();
                                    if(e.key=="m") return e.preventDefault();
                                    if( e.key=="2" || e.key=="3" || e.key=="4" || e.key=="5" || e.key=="6" || e.key=="7" || e.key=="8" || e.key=="9" || e.key=="1" || e.key=="0") 
                                    {
                                        if(this.props.values.korysnaplosha.toString().indexOf(".")>-1)
                                        {
                                            let index1 = this.props.values.korysnaplosha.toString().indexOf(".");
                                            let str1 = this.props.values.korysnaplosha.toString().slice(index1,this.props.values.korysnaplosha.toString().length );
                                            if(str1.length>1) return e.preventDefault();//znakiv pislia komu
                                        }
                                     
                                    } 
                                  }}
                                onChange={(e,v)=>  { 
                                    if(!Number(e.target.value)&& e.target.value.length>=1 
                                    && e.target.value!="1" 
                                    && e.target.value!="2"
                                    && e.target.value!="3"
                                    && e.target.value!="4"
                                    && e.target.value!="5"
                                    && e.target.value!="6"
                                    && e.target.value!="7"
                                    && e.target.value!="8"
                                    && e.target.value!="9"
                                    ) return;
                                    if(e.target.value.length<=6){//dovznyna vvody
                                            if(e.target.value!="0")this.props.handleChange(e,v);
                                        }
                                }}
                                onBlur={this.props.handleBlur}
                                value={this.props.values.korysnaplosha}
                                margin={"dense"}
                                style = {{marginRight: "15px"}}
                                inputProps={{
                                maxLength: 5
                                }}
                            />
                            </Grid>
                            <Grid item  md={4}  xs={4} sm={4}>
                            <TextField variant="outlined"
                                label="Кухня"
                                error={this.props.touched.kuchniplosha && Boolean(this.props.errors.kuchniplosha)}
                                display="inline"
                                type="text" 
                                name="kuchniplosha" 
                                id="kuchniplosha" 
                                onKeyDown={e => {
                                    if(this.props.values.kuchniplosha.length>6) return e.preventDefault();//dovznyna vvody
                                    if(e.key=="+") return e.preventDefault();
                                    if(e.key=="-") return e.preventDefault();
                                    if(e.key=="Enter") return e.preventDefault();
                                    if(e.key=="e") return e.preventDefault();
                                    if(e.key=="m") return e.preventDefault();
                                    if( e.key=="2" || e.key=="3" || e.key=="4" || e.key=="5" || e.key=="6" || e.key=="7" || e.key=="8" || e.key=="9" || e.key=="1" || e.key=="0") 
                                    {
                                        if(this.props.values.kuchniplosha.toString().indexOf(".")>-1)
                                        {
                                            let index1 = this.props.values.kuchniplosha.toString().indexOf(".");
                                            let str1 = this.props.values.kuchniplosha.toString().slice(index1,this.props.values.kuchniplosha.toString().length );
                                            if(str1.length>1) return e.preventDefault();//znakiv pislia komu
                                        }
                                     
                                    } 
                                  }}
                                 onChange={(e,v)=>  { 
                                    if(!Number(e.target.value)&& e.target.value.length>=1 
                                    && e.target.value!="1" 
                                    && e.target.value!="2"
                                    && e.target.value!="3"
                                    && e.target.value!="4"
                                    && e.target.value!="5"
                                    && e.target.value!="6"
                                    && e.target.value!="7"
                                    && e.target.value!="8"
                                    && e.target.value!="9"
                                    ) return;
                                    if(e.target.value.length<=6){//dovznyna vvody
                                            if(e.target.value!="0")this.props.handleChange(e,v);
                                        }
                                }}
                                onBlur={this.props.handleBlur}
                                value={this.props.values.kuchniplosha}
                                margin={"dense"}
                                hidden={this.props.state.type==4||this.props.state.type==5||this.props.state.type==6}
                                inputProps={{
                                maxLength: 5
                                }}
                            />
                            </Grid>
                        </Grid>
                        <SanvyzolFields  values={this.props.values}   setFieldValue={this.props.setFieldValue}
                             display={this.props.state.type==1}
                        />
                        <KstsanvuzlivField  handleChange={this.props.handleChange} values={this.props.values} touched={this.props.touched} errors={this.props.errors}
                             display={this.props.state.type==2||this.props.state.type==3||this.props.state.type==4}
                        />

                        <VilneplanuvanniaField  values={this.props.values}   setFieldValue={this.props.setFieldValue}
                             display={this.props.state.type==2||this.props.state.type==3||this.props.state.type==4}
                        />
 
                        <FormControl>
                            <TextField variant="outlined" required
                            style={{marginBottom:"7px"}}
                            select
                            error={this.props.touched.opalennia && Boolean(this.props.errors.opalennia)}
                            label="Опалення"
                            name="opalennia"
                            id="opalennia"
                            value={this.props.values.opalennia}
                            margin={"dense"}
                            onChange={(e)=>{this.props.handleChange(e);
                                
                            }}

                            placeholder="Виберіть опалення"
                            >
                            <MenuItem value={1}>без опалення</MenuItem>
                            <MenuItem value={2}>центральне</MenuItem>
                            <MenuItem value={3}>пічне</MenuItem>
                            <MenuItem value={4}>індивідуальне</MenuItem>
                            <MenuItem value={5}>електро</MenuItem>
                            <MenuItem value={6}>будинкове</MenuItem>
                            <MenuItem value={7}>твердопаливний котел</MenuItem>
                            </TextField>
                        </FormControl>
                    <FormControl>
                        <TextField
                            variant="outlined"
                            label="Висота стелі"
                            display="inline"
                            error={this.props.touched.vysotasteli && Boolean(this.props.errors.vysotasteli)}
                            type="text" 
                            name="vysotasteli" 
                            id="vysotasteli" 
                            margin={"dense"}
                           
                            onKeyDown={e => {
                                    if(this.props.values.vysotasteli.length>6) return e.preventDefault();
                                    if(e.key=="+") return e.preventDefault();
                                    if(e.key=="-") return e.preventDefault();
                                    if(e.key=="Enter") return e.preventDefault();
                                    if(e.key=="e") return e.preventDefault();
                                    if(e.key=="m") return e.preventDefault();
                                    if( e.key=="2" || e.key=="3" || e.key=="4" || e.key=="5" || e.key=="6" || e.key=="7" || e.key=="8" || e.key=="9" || e.key=="1" || e.key=="0") 
                                    {
                                        if(this.props.values.vysotasteli.toString().indexOf(".")>-1)
                                        {
                                            let index1 = this.props.values.vysotasteli.toString().indexOf(".");
                                            let str1 = this.props.values.vysotasteli.toString().slice(index1,this.props.values.vysotasteli.toString().length );
                                            if(str1.length>2) return e.preventDefault();
                                        }
                                     
                                    } 
                                  }}
                            value={this.props.values.vysotasteli}

                            onChange={(e,v)=>  { 
                                if(!Number(e.target.value)&& e.target.value.length>=1 
                                && e.target.value!="1" 
                                && e.target.value!="2"
                                && e.target.value!="3"
                                && e.target.value!="4"
                                && e.target.value!="5"
                                && e.target.value!="6"
                                && e.target.value!="7"
                                && e.target.value!="8"
                                && e.target.value!="9"
                                ) return;
                                 if(e.target.value.length<=6){
                                        if(e.target.value!="0")this.props.handleChange(e,v);
                                    }
                                }}
                        />
                    </FormControl>
                    
                    
                    <FormControl>
                            <TextField variant="outlined"
                            style={{marginBottom:"7px"}}
                            select
                            error={this.props.touched.kstbalkonivextended && Boolean(this.props.errors.kstbalkonivextended)}
                            label="Кі-сть балконів"
                            name="kstbalkonivextended"
                            id="kstbalkonivextended"
                            value={this.props.values.kstbalkonivextended}
                            margin={"dense"}
                            onChange={(e)=>{this.props.handleChange(e);
                                
                            }}

                            placeholder="Виберіть к-сть"
                            >
                            <MenuItem value={1}>1 балкон</MenuItem>
                            <MenuItem value={2}>1 лоджія</MenuItem>
                            <MenuItem value={3}>1 тераса</MenuItem>
                            <MenuItem value={4}>1 тераса +1</MenuItem>
                            <MenuItem value={5}>2</MenuItem>
                            <MenuItem value={6}>3</MenuItem>
                            <MenuItem value={7}>4</MenuItem>
                            <MenuItem value={8}>5+</MenuItem>
                        </TextField>
                    </FormControl>
                    <FormControl>
                            <FormControlLabel
                                control={
                                <Checkbox name="avtomisce"  value={this.props.values.avtomisce}  onClick={(event)=>{ this.props.setFieldValue("avtomisce",Boolean(event.target.checked));}}/>
                                }
                                label="Автомісце"
                            />
                    </FormControl>
                    <FormControl>
                        <FormControlLabel
                                control={
                                <Checkbox name="pidval"  value={this.props.values.pidval}  onClick={(event)=>{ this.props.setFieldValue("pidval",Boolean(event.target.checked));}}/>
                                }
                                label="Підвал"
                        />
                    </FormControl>

                        <FormControl>
                            <TextField variant="outlined" required
                            style={{marginBottom:"7px"}}
                            select
                            error={this.props.touched.stankim && Boolean(this.props.errors.stankim)}
                            label="Стан"
                            name="stankim"
                            id="stankim"
                            value={this.props.values.stankim}
                            margin={"dense"}
                            onChange={(e)=>{this.props.handleChange(e);
                                
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
                    <FormControl>
                        <TextField
                            variant="outlined"
                            label="Опис стану та ін."
                            display="inline"
                            error={this.props.touched.opys_stanu && Boolean(this.props.errors.opys_stanu)}
                            type="text" 
                            name="opys_stanu" 
                            id="opys_stanu" 
                            multiline   
                            margin={"dense"}
                            
                        />
                    </FormControl>
                    <FormControl>
                        <InputLabel>Вхід в приміщення</InputLabel>
                        <Select variant="outlined"
                            multiple
                            error={this.props.touched.vxidvprymishennia && Boolean(this.props.errors.vxidvprymishennia)}
                            label="Вхід в приміщення"
                            name="vxidvprymishennia"
                            id="vxidvprymishennia"
                            value={this.props.values.vxidvprymishennia}
                            margin={"dense"}
                            onChange={(e)=>{this.props.handleChange(e);
                            }}
                            renderValue={selected => (
                                        <div >
                                        {selected.map(value => (
                                            <Chip key={value} label={value}  />
                                        ))}
                                        </div>
                                    )}
                            placeholder="Виберіть вхід"
                            MenuProps={MenuProps}
                            >
                            <MenuItem value={"Фасадний"}>Фасадний</MenuItem>
                            <MenuItem value={"З підїзду"}>З підїзду</MenuItem>
                            <MenuItem value={"З двору"}>З двору</MenuItem>
                            <MenuItem value={"2фасадні"}>2 фасадні</MenuItem>
                        </Select>
                    </FormControl>

                    <FormControl>
                    
                              <TextField variant="outlined"
                                  label="Паркомісць"
                                  display="inline"
                                  error={this.props.touched.parkomisc && Boolean(this.props.errors.parkomisc)}

                                  type="number"
                                  name="parkomisc" 
                                  id="parkomisc" 
                                  inputProps={{ min: "1", max: "9999", step: "1" }}
                                  pattern='[0-9]{4}'
                                  onKeyDown={e => {
                                    if(this.props.values.parkomisc.length>4) return e.preventDefault();
                                    if(e.key=="+") return e.preventDefault();
                                    if(e.key=="-") return e.preventDefault();
                                    if(e.key=="Enter") return e.preventDefault();
                                    if(e.key=="e") return e.preventDefault();
                                    if(e.key=="m") return e.preventDefault();
                                    if(e.key==".") return e.preventDefault();
                                    if(e.key==",") return e.preventDefault();
                                  }}
                                  margin={"dense"}
                                  value={this.props.values.parkomisc}
                                  onChange={(e,v)=>  { if(e.target.value.length<=4){if(e.target.value!="0")this.props.handleChange(e,v);}}} 
                                  onBlur={this.props.handleBlur}
                              />
                           
                            </FormControl>
                    
                    
                        </FormGroup>
        
                        </ExpansionPanel>
            );
           }

           else{
             return null;
           }
        }
   }