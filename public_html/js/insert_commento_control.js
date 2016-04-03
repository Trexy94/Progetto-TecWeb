//funzione che svuota il testo delle form al focus
function delTextFocus(el){
	if(el.value === el.defaultValue){
		el.value="";
	}
}

//funzione per il controllo della correttezza del campi
function valida_commento(){

	var errore = "err_commento";

	//se settati svuoto gli span di errore
	if (document.getElementById(errore) !== "") {
	    document.getElementById(errore).innerHTML = "";
	}

	var commento = document.getElementById("form_commento").value;	
        var nome=document.getElementById("user").value;
        var email=document.getElementById("email").value;
        //verifico il pattern dell'email
        if (email.replace(/^\s+/g, '').length && !(/^([\w\-\+\.]+)@([\w\-\+\.]+).([\w\-\+\.]+)$/).test(email))
        {
           document.getElementById("err_commento").innerHTML = "L'email non &egrave; corretta.";
           return false;
        }
	//Effettua il controllo sui campi, se sono vuoti o composti da soli spazi
	if (!commento.replace(/^\s+/g, '').length  || !nome.replace(/^\s+/g, '').length || (commento === "Inserisci un commento")) {
            document.getElementById("err_commento").innerHTML = "Il campo nome e il commento sono obbligatori";
	    document.getElementById("form_commento").focus();
	    document.getElementById("form_commento").select();
	    return false;
	}
	else { //Finiti i controlli confermo
            return true;
	}
}
