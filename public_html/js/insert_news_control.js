//funzione che svuota il testo delle form al focus
function delTextFocus(el){
	if(el.value === el.defaultValue){
		el.value="";
	}
}

//funzione che va a riempire i campi della form con esempi 
function controlli(){
		var elem = document.getElementById("form_alt");
		elem.defaultValue = "contenuto tag alt";
                var elem2= document.getElementById("form_titolo");
		elem2.defaultValue = "titolo visualizzato nella home";
	document.getElementById("form_contenuto").innerHTML = "Inserire qui il testo completo della notizia.";
}

//funzione per il controllo dei campi
function validanotizia(){
var vettore = ["err_titolo", "err_alt", "err_corpo"];
                                    
	// svuoto gli span di errore
	for (i=0; i<3; i++) {
		if (document.getElementById(vettore[i]) !== "") {
			document.getElementById(vettore[i]).innerHTML = "";
		}
	}

	var alt = document.getElementById("form_alt").value;
	var titolo = document.getElementById("form_titolo").value;
	var contenuto = document.getElementById("form_contenuto").value;
        
	//Effettua il controllo sul campo alt
	if ((alt === "") || (alt === "undefined") || (alt === "contenuto tag alt")) {
		document.getElementById("err_alt").innerHTML = "Il campo &egrave; obbligatorio.";
	    document.getElementById("form_alt").focus();
	    document.getElementById("form_alt").select();
	    return false;
	}
        //Effettua il controllo sul campo titolo
        else if ((titolo === "") || (titolo === "undefined") || (titolo === "titolo visualizzato nella home")) {
		document.getElementById("err_titolo").innerHTML = "Il campo &egrave; obbligatorio.";
	    document.getElementById("form_titolo").focus();
	    document.getElementById("form_titolo").select();
	    return false;	
	}                //Effettua il controllo sul campo contenuto
	else if ((contenuto === "") || (contenuto === "undefined") || (contenuto === "Inserire qui il testo completo della notizia.")) {
	    document.getElementById("err_corpo").innerHTML = "Il campo &egrave; obbligatorio.";
	    document.getElementById("form_contenuto").focus();
	    document.getElementById("form_contenuto").select();
	    return false; 
	}
	else { //Finiti i controlli se tutto va bene invio i dati
return true;
	}
}
