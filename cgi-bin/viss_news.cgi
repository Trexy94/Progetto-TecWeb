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
use HTML::Parser;
use HTML::Entities;

# includo la mia libreria funzioni
require ('libreria_funzioni.pl');

# leggo l'id da get
my $cgi = new CGI;

my $id = $cgi->param('id');

# recupero dal file news xml i dati della news
my $file = "../data/news.xml";

# creazione oggetto parser
my $parser = XML::LibXML->new();

# apertura file e lettura input
my $doc = $parser->parse_file($file);


my $notizia = $doc->findnodes("/news/notizia[\@\id = $id]")->get_node(1);

        my $img = $notizia->findvalue('img');
        my $alt = decode_entities($notizia->findvalue('alt'));
	my $titolo = decode_entities($notizia->findvalue('titolo'));
        my $corpo = decode_entities($notizia->findvalue('testocontenuto'));
	my $data = $notizia->findvalue('datainserimento');

# stampo la pagina della news
print "Content-type:text/html\n\n";
print <<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
	<head>
	<title>News-Judo Club Castelfranco Veneto</title>
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
					 <div class="navigazione">Sei qui: <a href="./Home.cgi"> <span lang="en">Home</span></a> &gt;&gt; <span lang="en">News</span></div>
EOF
print " <div><h1 class=\"titolonews\"> $titolo</h1>
        <img src=\"$img\" alt=\"$alt\" class=\"imgnews\"\/>
        <div class=\"contenuto\">Scritto in data $data <p>$corpo</p></div>";
print '</div>
     <div class="footer"> <img class="valido" alt="css valido" src="../img/cssvalido.png"/><div class="indirizzo"> Via Boito, Castelfranco Veneto</div><img class="valido" alt="xhtml valido" src="../img/xhtmlvalido.png"/></div> <!-- mettere simboli w3c e html css valido-->    
    </body>
</html>';
