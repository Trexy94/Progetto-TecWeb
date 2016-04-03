#!/usr/bin/perl -w

# file che cambia password
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
my $id;

if(!($session->is_expired) || !($session->is_empty)){
	# ricavo l'autenticazione
	 $auth= $session->param('auth');
         $id=$session->param('username');
}
#basta controllare la stringa, perchè i non autenticati non hanno cookie e quindi dovrebbero conoscere la "magic word" e come è strutturato il login per craccarlo
if(($auth eq "amministratoreautenticato") && ($id))
{
my $cgi = new CGI;
my $pass = trim($cgi->param('newpassword'));
if (!$pass)
{
# stampo pagina di errore
my $err_msg = "la password non deve essere vuota";
&errore($err_msg);
exit;
}
	my $file = "../data/utenti.xml";
	
	# creazione oggetto parser
	my $parser = XML::LibXML->new();
	
	# apertura file e lettura input
	my $doc = $parser->parse_file($file);
	
	# estrazione radice
	my $root = $doc->getDocumentElement;

			# mi posiziono sul nodo da eliminare
			my $node = $doc->findnodes("/utenti/utente/username[text()='$id']")->get_node(1);
			#se non esiste lo username qui si pianta(quindi non è exploitabile per inserire utenti che non c'erano prima)
			# trovo il nonno(salgo 2 volte)
			my $parent = $node->parentNode;
                        my $grandparent = $parent->parentNode;
			# elimino il nodo(dal nonno tolgo il padre)
			$grandparent->removeChild($parent);

	# ricreo l'utente
	my $utente = XML::LibXML::Element->new('utente');
	
	my $username = XML::LibXML::Element->new('username');
	$username->appendText($id);
	$utente->appendChild($username);

	my $password = XML::LibXML::Element->new('password');
	$password->appendText($pass);
	$utente->appendChild($password);
	
$root->appendChild($utente);
	
	open(OUT,">$file") or die $!;
	print OUT $doc->toString;
	close(OUT);	
	print "Content-type:text/html\n\n";

print <<EOF;

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
	<head>
	<title>Successo-Judo Club Castelfranco Veneto</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <base href=""/>
		<link rel="icon" type="image/png" href="../img/TaoIco.png"></link>
        <link href="../css/Main.css" rel="stylesheet" type="text/css" media="screen"/>
        <link href="../css/print.css" rel="stylesheet" type="text/css" media="print"/>
         <link href='http://fonts.googleapis.com/css?family=Shojumaru' rel='stylesheet' type='text/css'/>

    </head>
    <body>
		 		<div><a href="Home.cgi"><img class="tao" alt="tao" src="../img/TaoLogo.png"/></a><div class="titolo"><a href="Home.cgi"><span lang="en">Judo Club</span></a></div><div class="sottotitolo"><a href="Home.cgi">Castelfranco Veneto</a></div></div>
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
		
		<div class="navigazione">Sei qui: Cambio avvenuto con successo</div>
		
        <div class="corpo">
Cambio avvenuto con successo, torna pure alla torna alla <a href=\"$ENV{HTTP_REFERER}\">pagina precedente</a></div>
        
        <div class="footer"> <img class="valido" alt="css valido" src="../img/cssvalido.png"/><div class="indirizzo"> Via Boito, Castelfranco Veneto</div><img class="valido" alt="xhtml valido" src="../img/xhtmlvalido.png"/></div> <!-- mettere simboli w3c e html css valido-->
        
        
    </body>
</html>
EOF
}
else
{
&errore_permessi();
}
