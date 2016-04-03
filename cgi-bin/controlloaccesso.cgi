#!/usr/bin/perl -w

# file che controlla l'accesso utente
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


# leggo i dati dal POST e li inserisco nell'hash DATI
my %DATI = &leggi_post();

if(!%DATI){
	print redirect("../cgi-bin/Home.cgi");
}

# creo e inizializzo le variabili con i dati del post
my $username = $DATI{'username'};
my $password = $DATI{'password'};
my $auth="amministratoreautenticato";
my $file = "../data/utenti.xml";

# creazione oggetto parser
my $parser = XML::LibXML->new();

# apertura file e lettura input
my $doc = $parser->parse_file($file);

# estrazione radice
my $root = $doc->getDocumentElement;

# array degli elementi username
my @user = $root->getElementsByTagName('username');

# controllo che l'username fornito sia presente nell'array
# variabile di controllo
my $trovato = 0;

# controllo che l'userername sia presente nel file
for my $u (@user){
	$u = $u->to_literal();
	if($username eq $u){ # l'username è presente
		$trovato = 1;
		last;
	}
}

if($trovato){
	# se è presente controllo la password
	# prelevo il valore della password dal file xml dal nodo con username = a quella passata dal form
	my $pwd = $doc->findvalue("/utenti/utente[username=\"$username\"]/password");
	# confronto le password
	if ($pwd ne $password)
{
print "Content-type:text/html\n\n";

print <<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
	<head>
	<title>Errore-Judo Club Castelfranco Veneto</title>
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
                <li><a href="../cgi-bin/Home.cgi"><span lang="en">HOME</span></a></li>
            <li><a href="../storia.html">STORIA CLUB</a></li>
            <li><a href="../ilJudo.html">IL <span lang="ja">JUDO</span></a></li>
            <li><a href="../ilBJJ.html">IL <span lang="ja">JIU JITSU</span> BRASILIANO</a></li>
            <li><a href="../maestri.html">MAESTRI</a></li>
            <li><a href="../orari.html">ORARI</a></li>
            <li><a href="info_contatti.cgi">INFO &amp; CONTATTI</a></li>
            </ul>		
        </div>
		
		<div class="navigazione">Sei qui: errore</div>
		
        <div class="corpo"> <span lang="en">Password</span> sbagliata o vuota, riprova di nuovo <a href="./amministratore.cgi"><span lang="en">Login</span></a></div> 
        <div class="footer"> <img class="valido" alt="css valido" src="../img/cssvalido.png"/><div class="indirizzo"> Via Boito, Castelfranco Veneto</div><img class="valido" alt="xhtml valido" src="../img/xhtmlvalido.png"/></div> <!-- mettere simboli w3c e html css valido-->
  </body>
</html>
EOF
exit;
}
	if ($pwd eq $password){
		# controllo se la sessione esiste gia
		my $session = CGI::Session->load() or die $!;

		if($session->is_expired || $session->is_empty){
			# sessione non esiste quindi la creo
			my $session = new CGI::Session(undef, undef, {Directory=>'/tmp'});
			# aggiungo i parametri utente alla sessione
			$session->param("username", $username);
			$session->param("auth", $auth);

			# creo il cookie
			my $cookie1 = CGI::Cookie->new(-name => $session->name, -value => $session->id);
			my $cookie2 = CGI::Cookie->new(-name => "JCC", -value => $username);
                        my $cookie3 = CGI::Cookie->new(-name => "JCCA", -value => $auth);
			print header(-cookie => [$cookie1,$cookie2,$cookie3]);
			

print "Content-type:text/html\n\n";			# creo una pagina accesso effettuato
print <<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
	<head>
	<title>Login-Judo Club Castelfranco Veneto</title>
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
            <li><a href="../ilBJJ.html">IL <span lang="ja">JIU JITSU</span> BRASILIANO</a></li>
            <li><a href="../maestri.html">MAESTRI</a></li>
            <li><a href="../orari.html">ORARI</a></li>
            <li><a href="info_contatti.cgi">INFO &amp; CONTATTI</a></li>
            </ul>		
        </div>
		
		<div class="navigazione">Sei qui: Login</div>
		
        <div class="corpo"><span lang="en">Login</span> effettuato con successo $username, torna pure alla <a href="./Home.cgi"><span lang="en">Home</span></a></div> 
        <div class="footer"> <img class="valido" alt="css valido" src="../img/cssvalido.png"/><div class="indirizzo"> Via Boito, Castelfranco Veneto</div><img class="valido" alt="xhtml valido" src="../img/xhtmlvalido.png"/></div> <!-- mettere simboli w3c e html css valido-->
    </body>
</html>
EOF

		}
		else{
			# la sessione esiste
			# controllo l'esistenza del cookie
			my %cookie = CGI::Cookie->fetch;
			my $cook = $cookie{'JCCA'};
			my $cook2 = $cookie{'JCCA'};
			# se i 2 cookie fondamentali non sono presenti lo ricreo
			if(!defined $cook){
				# ricreo il cookie se mancante
				my $cookie3 = CGI::Cookie->new(-name => "JCCA", -value => $auth);
				print header(-cookie => $cookie3);				
			}
			if(!defined $cook2){
                        # ricreo il cookie se mancante
			my $cookie2 = CGI::Cookie->new(-name => "JCC", -value => $username);
				print header(-cookie => $cookie2);				
			}
			# creo una pagina accesso già  effettuato
						print "Content-type:text/html\n\n";

print <<EOF;

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
	<head>
	<title>Refresh-Judo Club Castelfranco Veneto</title>
		<link rel="icon" type="image/png" href="../img/TaoIco.png"></link>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <base href=""/>
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
            <li><a href="../ilBJJ.html">IL <span lang="ja">JIU JITSU</span> BRASILIANO</a></li>
            <li><a href="../maestri.html">MAESTRI</a></li>
            <li><a href="../orari.html">ORARI</a></li>
            <li><a href="info_contatti.cgi">INFO &amp; CONTATTI</a></li>
            </ul>		
        </div>
		
		<div class="navigazione">Sei qui: errore</div>
		
        <div class="corpo">
<span lang="en">Login</span> refreshato con successo $username, <span lang="en">cookie</span> refreshato, si consiglia di tenere i <span lang="en">cookie</span> attivi, torna pure alla <a href="./Home.cgi"><span lang="en">Home</span></a></div> 
        <div class="footer"> <img class="valido" alt="css valido" src="../img/cssvalido.png"/><div class="indirizzo"> Via Boito, Castelfranco Veneto</div><img class="valido" alt="xhtml valido" src="../img/xhtmlvalido.png"/></div> <!-- mettere simboli w3c e html css valido-->
    </body>
</html>
EOF

		}
	}
}
else
{
print "Content-type:text/html\n\n";

print <<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
	<head>
	<title>Errore-Judo Club Castelfranco Veneto</title>
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
                <li><a href="../cgi-bin/Home.cgi"><span lang="en">HOME</span></a></li>
            <li><a href="../storia.html">STORIA CLUB</a></li>
            <li><a href="../ilJudo.html">IL <span lang="ja">JUDO</span></a></li>
            <li><a href="../ilBJJ.html">IL <span lang="ja">JIU JITSU</span> BRASILIANO</a></li>
            <li><a href="../maestri.html">MAESTRI</a></li>
            <li><a href="../orari.html">ORARI</a></li>
            <li><a href="info_contatti.cgi">INFO &amp; CONTATTI</a></li>
            </ul>		
        </div>
		
		<div class="navigazione">Sei qui: errore</div>
		
        <div class="corpo"><span lang="en">login</span> sbagliato o vuoto, riprova di nuovo <a href="./amministratore.cgi"><span lang="en">Login</span></a></div> 
        <div class="footer"> <img class="valido" alt="css valido" src="../img/cssvalido.png"/><div class="indirizzo"> Via Boito, Castelfranco Veneto</div><img class="valido" alt="xhtml valido" src="../img/xhtmlvalido.png"/></div> <!-- mettere simboli w3c e html css valido-->
  </body>
</html>
EOF
}
