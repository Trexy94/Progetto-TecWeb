#!/usr/bin/perl -w

# carico le librerie
use strict;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use CGI::Cookie;
use XML::LibXML;
use File::Copy;
use URI;

# includo la mia libreria funzioni
require ('libreria_funzioni.pl');

# controllo se la sessione esiste gia
my $session = CGI::Session->load() or die $!;

my $auth = $session->param('auth');
# creo la pagina di login
print "Content-type:text/html\n\n";
print <<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
	<head>
	<title>Amministrazione-Judo Club Castelfranco Veneto</title>
        <link rel="icon" type="image/png" href="../img/TaoIco.png"></link>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <base href=""/>
        <link href="../css/Main.css" rel="stylesheet" type="text/css" media="screen"/>
        <link href="../css/print.css" rel="stylesheet" type="text/css" media="print"/>
                <link href="http://fonts.googleapis.com/css?family=Shojumaru" rel="stylesheet" type="text/css"/>
                <script type="text/javascript" src="../js/login_control.js"></script>
    </head>
    <body><div><a href="Home.cgi"><img class="tao" alt="tao" src="../img/TaoLogo.png"/></a><div class="titolo"><a href="Home.cgi"><span lang="en">Judo Club</span></a></div><div class="sottotitolo"><a href="Home.cgi">Castelfranco Veneto</a></div></div>
<div class="menu">
            <ul class="lista-menu">
                <li><a href="Home.cgi"><span lang="en">HOME</span></a></li>
            <li><a href="../storia.html">STORIA CLUB</a></li>
            <li><a href="../ilJudo.html">IL <span lang="ja">JUDO</span></a></li>
            <li><a href="../ilBJJ.html">IL <span lang="ja">JIU JITSU</span> BRASILIANO</a></li> <!--verificare col screen reader la lettura giusta della parola-->
            <li><a href="../maestri.html">MAESTRI</a></li>
            <li><a href="../orari.html">ORARI</a></li>
            <li><a href="info_contatti.cgi">INFO &amp; CONTATTI</a></li>
            </ul>		
        </div>
		<div class="navigazione">Sei qui: <span lang="en">Login</span></div>
		
        <div class="corpo">
        
<h2>Login</h2>
				<form class="corpo" id="form_login" method="post" action="./controlloaccesso.cgi" onsubmit="return valida_campi()">
                                                <p class="span_err" id="err_login" ></p>
                                                 <p> scrivi qui il tuo <span lang="en">username</span>
                                                 <input type="text" name="username" id="username"/></p>
                                                <p> scrivi qui la tua <span lang="en">password</span>
                                                 <input type="password" name="password" id="password"/>
						</p>
						<p><input type="submit" value="Inserisci"/></p>
				</form>
EOF
#offro solo il cambio password, un nuovo utente significherebbe che è presente un nuovo maestro, circostanza che richiederebbe di riscrivere l'html, quindi aggiornare anche l'XML avrebbe un costo minimo
#lascio visibile la password, per aiutare a ricordarla
if ($auth eq "amministratoreautenticato")
{
        print'<h2>Cambio <span lang="en">Password</span></h2><form class="cambio password" id="form_cambio_password" method="post" action="./cambiopassword.cgi" onsubmit="return controllo_vuoto()">
 <p>scrivi qui la tua nuova <span lang="en">password</span> 
<input type="text" name="newpassword" id="newpassword"/></p>
<p>
<input type="submit" value="Cambia"/></p>
</form>';
}
print '</div><div class="footer"> <img class="valido" alt="css valido" src="../img/cssvalido.png"/><div class="indirizzo"> Via Boito, Castelfranco Veneto</div><img class="valido" alt="xhtml valido" src="../img/xhtmlvalido.png"/></div>    
    </body>
</html>';
