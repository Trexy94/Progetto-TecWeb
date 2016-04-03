#!/usr/bin/perl -w

# file che controlla l'amministrazione del sito
# carico le librerie
use strict;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use XML::LibXML;
use File::Copy;
use utf8;
use URI;
use HTML::Parser;
use HTML::Entities;
# includo la mia libreria funzioni
require ('libreria_funzioni.pl');

my $session = CGI::Session->load();

my $auth;
if(!($session->is_expired) || !($session->is_empty)){
	# ricavo l'autenticazione
        $auth = $session->param('auth');
}

# recupero dal file commenti.xml i dati dei commenti.
my $file = "../data/commenti.xml";

# creazione oggetto parser
my $parser = XML::LibXML->new();

# apertura file e lettura input
my $doc = $parser->parse_file($file);


# stampo la pagina
print "Content-type:text/html\n\n";
print <<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
	<head>
        <title>Info e contatti-Judo Club Castelfranco Veneto</title>
        <link rel="icon" type="image/png" href="../img/TaoIco.png"></link>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <base href=""/>
        <link href="../css/Main.css" rel="stylesheet" type="text/css" media="screen"/>
        <link href="../css/print.css" rel="stylesheet" type="text/css" media="print"/>
                <link href='http://fonts.googleapis.com/css?family=Shojumaru' rel='stylesheet' type='text/css'/>
                <script type="text/javascript" src="../js/insert_commento_control.js"></script>
    </head>
    <body>
		 <div><a href="Home.cgi"><img class="tao" alt="tao" src="../img/TaoLogo.png"/></a><div class="titolo"><a href="Home.cgi"><span lang="en">Judo Club</span></a></div><div class="sottotitolo"><a href="Home.cgi">Castelfranco Veneto</a></div></div>
                               		 <div class="menu">
            <ul class="lista-menu">
                <li><a href="Home.cgi"><span lang="en">HOME</span></a></li>
            <li><a href="../storia.html">STORIA CLUB</a></li>
            <li><a href="../ilJudo.html">IL <span lang="ja">JUDO</span></a></li>
            <li><a href="../ilBJJ.html">IL <span lang="ja">JIU JITSU</span> BRASILIANO</a></li>
            <li><a href="../maestri.html">MAESTRI</a></li>
            <li><a href="../orari.html">ORARI</a></li>
            <li class="attivo">INFO &amp; CONTATTI</li>            
            </ul>		
        </div>		
		<div class="navigazione">Sei qui: <a href="./Home.cgi"><span lang="en">Home</span></a> &gt;&gt; Info &amp; Contatti</div>
		
        <div  class="corpo">
		
             <h2 class="testo_posizionato">Dove Siamo</h2>
            <p class="testo_centrato">Palestra della Scuola Elementare (Zona Est), Via Puccini (entrata Via Boito)</p>
        </div>
<h2>Commenti:</h2>
EOF
#<!-- <div id="frame"><iframe src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d11151.785033051181!2d11.912257207360048!3d45.67197917608955!3m2!1i1024!2i768!4f13.1!3m3!#1m2!1s0x47792944c89edead%3A0xff9b95279b5359b5!2sVia+Boito%2C+31033+Castelfranco+Veneto+TV!5e0!3m2!1sit!2sit!4v1417788429881"  id="frame2"></iframe></div>//non valida in xhtml #però, sarebbe stato bello metterlo ma non facciamo una pagina in html 5 solo per questo tag-->
# estrazione dei commenti
my @commenti = $doc->findnodes("/commenti/commento");

# stampa dei commenti
foreach my $commento (@commenti){
	my $user = decode_entities($commento->findvalue('user'));
	my $datac = $commento->findvalue('datacommento');
	my $testo = decode_entities($commento->findvalue('testo'));
        my $id = $commento->getAttribute('id');
        my $mail =decode_entities($commento->findvalue('email'));
	
	print "<div class=\"commenti\">
				<span class=\"commento_user\">Commento di : <strong>$user</strong></span>
				<span class=\"commento_data\">Scritto il : <strong>$datac</strong></span>
				<p>$testo</p>";
#basta controllare la stringa, perchè i non autenticati non hanno cookie e quindi dovrebbero conoscere la "magic word" e come è strutturato il login per craccarlo
	if($auth eq "amministratoreautenticato"){
        
		# stampo il bottone per eliminare il commento e la mail
		
                                print "
                                        <span class=\"email\">email :<strong>$mail</strong></span>
                                                <form action=\"elimina_commento.cgi\" class=\"form_commenti\" method=\"post\"><p>
						<input type=\"hidden\" name=\"user_commento\" value=\"$id\"/>
						<input type=\"submit\" name=\"elimina\" value=\"Elimina\"/>
					</p></form>";
	}
print "</div>";	
}
		# aggiungi commento
		print '<h2 id="scompari">scrivi qualcosa anche tu!</h2>
<noscript><p>il sistema dei commenti per funzionare al meglio necessita di javascript, per favore attivalo se vuoi utilizzare questa funzione</p></noscript>
				<form class="corpo" id="form_new_commento" method="post" action="../cgi-bin/insert_commento.cgi"  onsubmit="return valida_commento()">
<p class="span_err" id="err_commento"></p><p>
<span> scrivi qui il tuo nome(sar&agrave; visibile a tutti)</span></p>
<p><input type="text" name="user" id="user"/></p>
<p>Lascia pure un commento qui</p>
<p><textarea id="form_commento" name="commento" onfocus="delTextFocus(this)" rows="20" cols="50"></textarea></p>
<p> se vuoi essere ricontattato, lasciaci qui la tua email(non sar&agrave; visibile a nessuno a parte i nostri amministratori)</p>
<p><input type="text" name="email" id="email"/></p>
<p><input type="submit" value="Inserisci"/></p>
</form>';
print "<div class=\"testo_centrato\">

<h3>Per ulteriori informazioni:</h3>

<p>Tel.: 329 8472201 (Renzo Ondei)</p>

<p>340 3075123 (Silvio Cici)</p>

<p>mail: cicisilvio&#64;gmail.com</p>
                 </div>
        <div class=\"footer\"> <img class=\"valido\" alt=\"css valido\" src=\"../img/cssvalido.png\"/><div class=\"indirizzo\"> Via Boito, Castelfranco Veneto</div><a href=\"./amministratore.cgi\">Amministrazione</a><img class=\"valido\" alt=\"xhtml valido\" src=\"../img/xhtmlvalido.png\"/></div> <!-- mettere simboli w3c e html css valido-->  
</body>
</html>";
