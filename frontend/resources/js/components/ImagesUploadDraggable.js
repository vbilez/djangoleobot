import React, { Component, RadioButton,Fragment } from 'react';
import {Container, TextField, FormGroup, Button, RadioGroup, Select, 
        MenuItem, Box, FormControl, Radio,FormControlLabel, Grid, Checkbox
} from '@material-ui/core';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCoffee,faUpload } from '@fortawesome/free-solid-svg-icons';
import Typography from '@material-ui/core/Typography';
import LinearProgress from '@material-ui/core/LinearProgress';

 export default class ImagesUploadDraggable extends Component {
   constructor(props) {
    super(props);
	this.state={
		imgs:[],
		previews:[],
		photoindex:0,
		loadprogress:[]
	}


		this.state.previews[0] = {class:"empty"};
	
	
   }


	handleChange(e) {

		e.preventDefault();
		const filesList = e.target.files;

		if (filesList.length === 0) return;
		//Spread array to current state preview URLs
		let arr = this.state.imgs;
		let previewstate = this.state.previews;
		let photoindex = this.state.photoindex;
		let statename = this.props.statename;
		if(photoindex>this.props.imgcount-1) return;
		let len = filesList.length > this.props.imgcount ? this.props.imgcount : filesList.length;
		for (let i = 0; i < filesList.length; i++) {
			if(photoindex>this.props.imgcount-1) return;
			const file = filesList[i];

			const reader = new FileReader();
			previewstate[photoindex] = {class:"loading"};
			this.setState({previews: previewstate});
			reader.onloadstart = e =>{
				var loadprogressa = this.state.loadprogress;
					loadprogressa[photoindex]=e.loaded;
					this.setState({loadprogress: loadprogressa});
			}
			reader.onprogress = data => {
				if (data.lengthComputable) {                                            
					var progress = parseInt( ((data.loaded / data.total) * 100), 10 );
					var loadprogressa = this.state.loadprogress;
					loadprogressa[photoindex]=progress;
					this.setState({loadprogress: loadprogressa});
				}
        	}

			reader.onload = upload => {
				//push new image to the end of 
				arr.push(upload.target.result);
				//Set state to arr
				this.setState({imgs: arr});
				this.props.setState({[statename]: arr});
				previewstate[photoindex] = {class:"photo"};
				this.setState({previews: previewstate});
				photoindex=photoindex+1;
				this.setState({photoindex: photoindex});
				if(photoindex<=previewstate.length)
				{
					previewstate.push({class:"empty"});
					this.setState({previews: previewstate});
				}

			};
			reader.readAsDataURL(file);

		}
		console.log('photoindex'+photoindex);
		console.log('previewstate.length'+previewstate.length);
		
	};
	dragStart(e) {
		this.dragged = e.currentTarget;
		e.dataTransfer.effectAllowed = 'move';
		e.dataTransfer.setData('text/html', this.dragged);
	}

	dragOver(e) {
		e.preventDefault();
		
		//this.dragged.style.display = "none";
		//if(e.target.className === 'placeholder') return;
		this.over = e.target;
		//e.target.parentNode.insertBefore(placeholder, e.target);
	}

	 dragEnd(e) {
		//this.dragged.style.display = 'block';
		//this.dragged.parentNode.removeChild(placeholder);
		
		// update state
		var data = this.state.imgs;
		var from = Number(this.dragged.closest("li").attributes.getNamedItem('data-slot').value);
		var to = Number(this.over.closest("li").attributes.getNamedItem('data-slot').value);
		var drag = this.over.closest("li").attributes.getNamedItem('data-drag').value;
		let statename = this.props.statename;
		if(drag!='drag') return;
		if (from == to) return;
		console.log('moving from '+from+'to' +to);

		let temp = data[from];
		data[from] = data[to];
		data[to] = temp;
		this.setState({imgs: data});
		this.props.setState({[statename]: data});

	}


	rotateImage64(imageBase64, rotation, cb) {
			var img = new Image();
				img.src = imageBase64;
				img.onload = () => {
				var canvas = document.createElement("canvas");
				const maxDim = Math.max(img.height, img.width);
				if ([90, 270].indexOf(rotation) > -1) {
					canvas.width = img.height;
					canvas.height = img.width;
				} else {
					canvas.width = img.width;
					canvas.height = img.height;
				}
				var ctx = canvas.getContext("2d");
				ctx.setTransform(1, 0, 0, 1, maxDim / 2, maxDim / 2);
				ctx.rotate(90 * (Math.PI / 180));
				ctx.drawImage(img, -maxDim / 2, -maxDim / 2);
				cb(canvas.toDataURL("image/jpeg"));
				};
	}
	rotateImage = (i) =>{
		console.log(i);
	}

	
	removeImage = (i) => {
		let arr = this.state.imgs;
		let previewstate = this.state.previews;
		let photoindex = this.state.photoindex;
		let statename = this.props.statename;
		let loadprogressa = this.state.loadprogress;
		let lip = false;
		let lil = false;
		let lastindex=0;
		let previewKeys = previewstate.map(el=>el.class);
		let liphoto = previewKeys.lastIndexOf("photo");
		let liloading = previewKeys.lastIndexOf("loading");
		arr.splice(i,1);
		if(liphoto>-1)
		{
			lip=true;
			if(liphoto>lastindex)
			{
				lastindex=liphoto;
			}

		}

		if(liloading>-1)
		{
			lip=true;
			if(liloading>lastindex)
			{
				lastindex=liloading;
			}

		}
		
		//previewstate[i] = {class:"empty"};
		previewstate.splice(i, 1);
		/*
		if(i!=lastindex)
		{
			let a = previewstate[lastindex];
			previewstate[lastindex] = {class:"empty"};
			previewstate[i] = a;
		}
		*/
		
		loadprogressa.splice(i,1);
		photoindex=photoindex-1;
		this.setState({imgs: arr});
		this.props.setState({[statename]: arr});
		this.setState({previews: previewstate});
		this.setState({photoindex: photoindex});
		this.setState({loadprogress: loadprogressa});

	};
	triggerInputFile = () => this.fileInput.click();
	render(){
	const data = this.state.previews;

	if(this.props.display){
	return (
    <React.Fragment>
	
	<div style={{align:"center", textAlign:"center",marginTop:"5px"}}>
							<Typography>{this.props.caption} ({this.props.imgcount} макс)</Typography><Button variant="contained"  onClick={this.triggerInputFile}
												style=
												{{backgroundColor:"#b71c1c", color:"white"}}>&nbsp;&nbsp;&nbsp;&nbsp;+ Фото</Button>
						  </div>
        <input  style={{display:"none"}} ref={fileInput => this.fileInput = fileInput}  type="file" multiple accept="image/*" onChange={this.handleChange.bind(this)} />
		 
        <div style={{marginBottom:"20px", clear:"both"}}></div>
		
        <div className="fleft clr rel focusbox">
			<ul className="photos-show-mini clr ui-sortable photoul" onDragOver={this.dragOver.bind(this)}>
			{data.map((d, idx)=>{
				const fc =  idx==0?'first-child':'';
				let photoclases = 'fleft with-photo br2 rel limargin' + fc;
				if(d.class=="empty") return	(<li key={idx} onClick={this.triggerInputFile} className="fleft empty rel limargin" data-slot={idx} style={{zIndex: '0'}}>
						<div className="br5">
							<a href="#" className="block tcenter" title="Добавить фото">
                                <i data-icon="plus"></i>
							</a>
						</div>
					</li>);
				if(d.class=="loading") return (<li key={idx} onClick={this.triggerInputFile} className="fleft empty rel limargin" data-slot={idx} style={{zIndex: '0'}}>
				
						<div className="br5">
						
							<a href="#" className="block tcenter" title="Добавить фото">
                                <FontAwesomeIcon icon={faUpload} style={{marginTop:"25px"}}/>
							</a>
							<LinearProgress variant="determinate" value={this.state.loadprogress[idx] ||0} />
						</div>
						
					</li>
					);
        		if(d.class=="photo") return (<li key={idx} draggable={true} onDragStart={this.dragStart.bind(this)}  data-drag={"drag"} data-slot={idx} onDragEnd={this.dragEnd.bind(this)} className={photoclases} id={"add-img-".idx} style={{position: 'relative', left: '0px', top: '0px'}}>
							<div>
								<a className="rotate-photo-a"  title="Изменить фото" href="#" rel="1" >
									<i data-icon="circle_rotate"  onClick={() =>{this.rotateImage(idx)}}></i>
								</a>
								<a className="delete-photo-a" title="Удалить" href="#" rel="1">
									<i data-icon="circle_remove" onClick={() =>{this.removeImage(idx)}}></i>
								</a>
								<img className="" src={this.state.imgs[idx] || ""} id={"img_".idx} alt="" ></img>
							</div>
						</li>);
       })}
                    
			</ul>

		</div>
        <div className="clr"></div>
     </React.Fragment>
            );
           }

           else{
             return null;
           }
        }
   }

   