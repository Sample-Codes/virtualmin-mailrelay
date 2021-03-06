#!/usr/local/bin/perl
# Show a form for editing a mail relay domain's destination server
use strict;
use warnings;
our (%text, %in);

require 'virtualmin-mailrelay-lib.pl';
&ReadParse();

# Get and check the domain
&can_edit_relay($in{'dom'}) || &error($text{'edit_ecannot'});
my $d = &virtual_server::get_domain_by("dom", $in{'dom'});
$d || &error($text{'edit_edomain'});
my $relay = &get_relay_destination($in{'dom'});
$relay || &error($text{'edit_erelay'});

&ui_print_header(&virtual_server::domain_in($d), $text{'edit_title'}, "");

print &ui_form_start("save.cgi");
print &ui_hidden("dom", $in{'dom'});
print &ui_table_start($text{'edit_header'}, undef, 2);

# Relay destination
print &ui_table_row($text{'edit_relay'},
	&ui_textbox("relay", $relay, 30));

# Filter spam?
if (&can_domain_filter()) {
	print &ui_table_row($text{'edit_filter'},
		&ui_yesno_radio("filter", &get_domain_filter($d->{'dom'})));
	}

print &ui_table_end();
print &ui_form_end([ [ undef, $text{'save'} ] ]);

# Show mail queue for this domain
if (&supports_mail_queue() && $relay) {
	print &ui_hr();
	print &ui_subheading($text{'edit_queue'});

	my @queue = &list_mail_queue($d);
	print &ui_columns_table(
		[ $text{'edit_from'}, $text{'edit_to'},
		  $text{'edit_date'}, $text{'edit_size'} ],
		"100%",
		[ map { [ $_->{'from'}, $_->{'to'},
			  $_->{'date'}, &nice_size($_->{'size'}) ] } @queue ],
		undef,
		0,
		undef,
		$text{'edit_noqueue'});
	}

&ui_print_footer("/", $text{'index'});
