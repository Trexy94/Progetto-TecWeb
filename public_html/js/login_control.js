
function valida_campi(){

	var errore = "err_login";

	//se settati svuoto gli span di errore
	if (document.getElementById(errore) !== "") {
	    document.getElementById(errore).innerHTML = "";
	}

	var username = document.getElementById("username").value;	
        var password=document.getElementById("password").value;
        
        if (!username.replace(/^\s+/g, '').length || !password.replace(/^\s+/g, '').length)
        {
           document.getElementById(errore).innerHTML = "tutti i campi sono obbligatori.";
           return false;
	}
	else { //Finiti i controlli do l'ok
                return true;
	}
}
function controllo_vuoto(){
    var pass = document.getElementById("newpassword").value;
      if (!pass.replace(/^\s+/g, '').length)
      {
          alert("La nuova password non deve essere vuota!!");
          return false;
      }
      else
          return true;
    }
