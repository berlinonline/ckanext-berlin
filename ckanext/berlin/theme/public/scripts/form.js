window.onload = function(){
	var form = document.forms["package-edit"];

	// store 'language' and 'apiurl' in correct field
	for(counter=0;;counter++){
		if(form.elements["resources__"+counter+"__description"]==null) break;

		var description = form.elements["resources__"+counter+"__description"];

		var strings = description.value.split(" | ");

		if(strings.length == 1)
			description.value = strings[0];
		if(strings.length == 2){
			description.value = strings[0];
			form.elements["resources__"+counter+"__language"].value = strings[1];
		}
		if(strings.length == 3){
			description.value = strings[0];
			form.elements["resources__"+counter+"__language"].value = strings[1];
			form.elements["resources__"+counter+"__apiurl"].value = strings[2];
		}
	}
};

function validateForm(){
	var form = document.forms["package-edit"];
	
	// get all required information
	var title = form.elements["title"].value;
	var packagename = form.elements["name"].value;
	var author = form.elements["author"].value;
	var maintainer_mail = form.elements["maintainer_email"].value;
	var license_id = form.elements["license_id"].value;
	var date_released = form.elements["extras__1__value"].value;
	var date_updated = form.elements["extras__2__value"].value;
	var tempCovFrom = form.elements["extras__3__value"].value;
	var tempCovTo = form.elements["extras__4__value"].value;
	var state = form.elements["state"].value;

	var summary = '';
	var counter;

	var urlPattern = /(ftp|https?):\/\/([-\w\.]+)+(:\d+)?(\/([\w/_\.]*(\?\S+)?)?)?/;

	// check if values are empty
	if (!packagename){
		alert("Name fehlt");
		return false;
	}

	// check if email has a correct formatting
	// this is NOT a check if it's a valid email address.
	if (!isValidEmail(maintainer_mail)){
		alert("Ungültige E-Mail Adresse");
		return false;
	}

	// check if date_released has a correct formatting
	if(!isValidDate(date_released)){
		alert("Falsches Format beim Veröffentlichungsdatum");
		return false;
	}

	// check if date_updated has a correct formatting (if date provided)
	if(date_updated != "" && !isValidDate(date_updated)){
		alert("Falsches Format beim Aktualisierungsdatum");
		return false;
	}

	// check if tempCovFrom has a correct formatting (if date provided)
	if(tempCovFrom != "" && !isValidDate(tempCovFrom)){
		alert("Falsches Format beim Datum des Zeitraums");
		return false;
	}
	
	// check if tempCovTo has a correct formatting (if date provided)
	if(tempCovTo != "" && !isValidDate(tempCovTo)){
		alert("Falsches Format beim Datum des Zeitraums");
		return false;
	}
	
	if (!title)
		summary += "Titel fehlt\n";
	if (!author)
		summary += "Veröffentlichende Stelle fehlt\n";
	if (!maintainer_mail)
		summary += "Kontakt E-Mail fehlt\n";
	if (!license_id)
		summary += "Lizenz fehlt\n";


	for(counter=0;;counter++){
		if(form.elements["resources__"+counter+"__url"]==null) break;

		// get required information
		var url = form.elements["resources__"+counter+"__url"].value;
		var format = form.elements["resources__"+counter+"__format"].value;
		var description = form.elements["resources__"+counter+"__description"].value;
		var language = form.elements["resources__"+counter+"__language"].value;

		// check if all fields are empty and it's the first row - need some
		// values
		if(!url && !format && !description && !language && counter == 0){
			alert("URL der "+ (counter+1) +". Datei fehlt");
			return false;		
		}
		// check if all fields are empty - skip this row
		if(!url && !format && !description && !language){
			continue;	
		}
	
		if(!url){
			alert("URL der "+ (counter+1) +". Datei fehlt");
			return false;
		}

		if(!urlPattern.test(url)){
			alert("URL der "+ (counter+1) +". Datei ist fehlerhaft. Sollte mit http:// anfangen.");
			return false;
		}

		if (!format)
			summary += "Format der "+ (counter+1) + ". Datei fehlt\n";
		if (!description)
			summary += "Beschreibung der "+ (counter+1) + ". Datei fehlt\n";
		if (!language){
			alert("Sprache der "+ (counter+1) +". Datei fehlt");
			return false;			
		}
		if(language.length!=2){
			alert("Sprache der "+ (counter+1) + ". Datei ist fehlerhaft. Bitte geben Sie z.B. 'de' ein.");
			return false;
		}					
	}

	if(summary == ''){
		if(state=="active"){ // active && complete
			moveDetailsToDescription(form,counter);
			return true;
		}
		else{ // inactive && complete
			var bool = confirm("Die Angaben sind vollständig, jedoch sind die Daten für andere nicht sichtbar.\n\nSoll der Status auf aktiv gesetzt werden?\n\nOK: Speichern und aktivieren\nAbbrechen: Speichern, aber nicht veröffentlichen.");
			if(bool){
				form.elements["state"].value="active";
				moveDetailsToDescription(form,counter);
				return true;			
			}
			else
				moveDetailsToDescription(form,counter);
				return true;
		}
	}
	else{
		if(state=="active"){ // active && incomplete
			var bool = confirm("Die Angaben sind unvollständig!\n\n"+summary+"\nDennoch abschicken? Die Metadaten werden zwar gespeichert, sind aber für Dritte nicht sichtbar.");
			if(bool){
				form.elements["state"].value="deleted";
				moveDetailsToDescription(form,counter);
				return true;
			}
			else
				return false;	
		}
		else{ // inactive && incomplete
			moveDetailsToDescription(form,counter);
			return true;
		}
	}
};



// checks if 'email' is a valid email-pattern
function isValidEmail(email){
	var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
	
	return emailPattern.test(email);
};

// checks if date has a valid date pattern
function isValidDate(date){
	if(date == "") return false;
	var datePattern = /^(19|20)\d\d[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])$/;

	return datePattern.test(date);
};

// adds 'language' and 'apiurl' to 'descr' in every row
function moveDetailsToDescription(form,counter){
	for(i=0;i<counter;i++){
		var description = form.elements["resources__"+i+"__description"];

		var lang = form.elements["resources__"+i+"__language"].value;
		var api = form.elements["resources__"+i+"__apiurl"].value;


		if(!lang && !api)
			continue;
		if(lang && !api)
			description.value += " | " + lang;
		if(!lang && api)
			description.value += " |  | " + api;
		if(lang && api)
			description.value += " | " + lang + " | " +api;
	}
};
