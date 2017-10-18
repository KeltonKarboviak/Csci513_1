#!/usr/bin/perl

use strict;
use CGI;

my $query = new CGI;
my $search_keywords = $query->url_param('search_keywords');

# Remove leading and trailing spacing
$search_keywords =~ s/^\s+|\s+$//g;

# For security, remove some Unix metacharacters
$search_keywords =~ s/"/\\"/g;

# Compose a Python command
my $cmd = "python SearchGames.py \"$search_keywords\"";

system($cmd);
