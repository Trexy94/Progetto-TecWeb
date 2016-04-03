#!/usr/bin/perl -w

# carico le librerie
use strict;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use CGI::Cookie;
use XML::LibXML;
use XML::LibXSLT;
use File::Copy;
use POSIX;
use URI;

# includo la mia libreria funzioni
require ('libreria_funzioni.pl');

# indirizzo pagina precedente
my $page_precedente = $ENV{HTTP_REFERER};

# leggo i dati dal post e li inserisco nell'hash DATI
my %DATI = &leggi_post();	
	
			if(!%DATI){
				# in caso l'admin carichi la pagina da url
				print redirect($ENV{HTTP_REFERER});
			}
			# Carico file utenti.xml
			my $file = "../data/commenti.xml";
		
			# creazione oggetto parser
			my $parser = XML::LibXML->new();
		
			# apertura file e lettura input
			my $doc = $parser->parse_file($file);
			
			# estraggo dal post i dati libro e comento del libro
			my $id = $DATI{'user_commento'};
						
			# mi posiziono sul nodo da eliminare
			my $node = $doc->findnodes("/commenti/commento[\@\id = $id]")->get_node(1);
			
			# trovo il padre
			my $parent = $node->parentNode;
			# elimino il nodo
			$parent->removeChild($node);
			
			# stampo modifiche
			# scrittura su file
			open(OUT,">$file") or die $!;
			print OUT $doc->toString;
			close(OUT);
			
			print "Location:info_contatti.cgi\n\n";
			
			
