#!/usr/bin/perl -w

# carico le librerie
use strict;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use CGI::Cookie;
use XML::LibXML;
use File::Copy;
use utf8;
use URI;

# includo la mia libreria funzioni
require ('libreria_funzioni.pl');


# controllo se la sessione esiste gia
my $session = CGI::Session->load();
my $auth;
if(!($session->is_expired) || !($session->is_empty)){
	# ricavo l'autenticazione
	 $auth= $session->param('auth');
}
#basta controllare la stringa, perchè i non autenticati non hanno cookie e quindi dovrebbero conoscere la "magic word" e come è strutturato il login per craccarlo
if($auth eq "amministratoreautenticato")
{
# stampo la pagina per l'admin
print "Content-type:text/html\n\n";
print <<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
	<head>
	<title>Aggiungi notizia-Judo Club Castelfranco Veneto</title>
	<link rel="icon" type="image/png" href="../img/TaoIco.png"></link>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <base href=""/>
        <link href="../css/Main.css" rel="stylesheet" type="text/css" media="screen"/>
        <link href="../css/print.css" rel="stylesheet" type="text/css" media="print"/>
                <link href='http://fonts.googleapis.com/css?family=Shojumaru' rel='stylesheet' type='text/css'/>
		<script type="text/javascript" src="../js/insert_news_control.js"></script>
	</head>
	<body onload="controlli()">
		 		<div><a href="Home.cgi"><img class="tao" alt="tao" src="../img/TaoLogo.png"/></a><div class="titolo"><a href="Home.cgi"><span lang="en">Judo Club</span></a></div><div class="sottotitolo"><a href="Home.cgi">Castelfranco Veneto</a></div></div>
                               		 <div class="menu">
            <ul class="lista-menu">
                <li><a href="Home.cgi"><span lang="en">HOME</span></a></li>
            <li><a href="../storia.html">STORIA CLUB</a></li>
            <li><a href="../ilJudo.html">IL <span lang="ja">JUDO</span></a></li>
            <li><a href="../ilBJJ.html">IL <span lang="ja">JIU JITSU</span> BRASILIANO</a></li>
            <li><a href="../maestri.html">MAESTRI</a></li>
            <li><a href="../orari.html">ORARI</a></li>
            <li><a href="info_contatti.cgi">INFO &amp; CONTATTI</a></li>
            </ul>		
        </div>    
					 <div class="navigazione">Sei qui: <a href="./Home.cgi"> <span lang="en">Home</span></a> &gt;&gt; Inserimento <span lang="en">news</span></div>
		<div class="corpo">
			<div class="display">
				<h2>Aggiungi notizia</h2>
<noscript><p>per una migliore usabilit&agrave;, si prega di attivare il javascript, per favore</p></noscript>
				<p>Per inserire una nuova notizia, compilare qui sotto. Tutti i campi sono obbligatori. sono accettate estensioni .png, .jpg, .jpeg, .gif e una dimensione inferiore a 5Mb per le immagini.</p>
				<form class="corpo" id="form_aggiungi_notizia" method="post" enctype="multipart/form-data" action="../cgi-bin/insert_notizia.cgi" onsubmit="return validanotizia()">
<p>
							Immagine:
							<input id="form_img" name="img" type="file" /></p>
							<p><span class="span_err" id="err_img"></span></p>
							<p>descrizione immagine:
							<input id="form_alt" name="alt" type="text" onfocus="delTextFocus(this)" /></p><p><span class="span_err" id="err_alt" ></span>
						</p>
							<p>Titolo:
							<input id="form_titolo" name="titolo" type="text" onfocus="delTextFocus(this)" /></p><p><span class="span_err" id="err_titolo"></span>
						</p>
							<p>Corpo della notizia:
							<textarea id="form_contenuto" name="contenuto" onfocus="delTextFocus(this)" rows="20" cols="50">
							</textarea></p><p><span class="span_err" id="err_corpo" ></span>
						</p>
						<p><input type="submit" value="Inserisci"/></p>
				</form>
			</div>
		</div>
     <div class="footer"> <img class="valido" alt="css valido" src="../img/cssvalido.png"/><div class="indirizzo"> Via Boito, Castelfranco Veneto</div><img class="valido" alt="xhtml valido" src="../img/xhtmlvalido.png"/></div> <!-- mettere simboli w3c e html css valido-->    
    </body>
</html>
EOF
}
else
{
&errore_permessi();
}
