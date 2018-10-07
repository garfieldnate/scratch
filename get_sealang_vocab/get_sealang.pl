#!/usr/bin/env perl
use HTTP::Tiny;
use feature 'say';
use URI::Escape;
use Path::Tiny;
use HTML::TableExtract;


sub get_categories {
    my $url = 'http://www.sealang.net/thai/vocabulary/menu.htm';

    my $response = HTTP::Tiny->new->get($url);
    if (!$response->{success}) {
        say "Couldn't download $url";
    }
    my $html = $response->{content};
    my @categories;
    while($html =~ m/onClick="list\.value='([^']+)';/g) {
        push @categories, $1;
    }
    \@categories;
}

sub download_vocab {
    my ($cats) = @_;
    my $base_url = 'http://www.sealang.net/thai/vocabulary/search.pl?list=';
    my @vocab;
    for my $cat (@$cats) {
        my $url = $base_url . uri_escape($cat);
        say "downloading $url";
        my $response = HTTP::Tiny->new->get($url);
        if (!$response->{success}) {
            say "Couldn't download $url";
        } else {
            # extract the table of vocab and add an extra column containing the category
            my $html = $response->{content};
            # these mess up the output
            $html =~ s/&nbsp;//sg;
            my $te = HTML::TableExtract->new( headers => [qw(WebRank term gloss)] );
            $te->parse($html);
            foreach my $row ($te->rows) {
                unshift @$row, $cat;
                push @vocab, $row;
            }
        }
        # give the sealang servers a break :)
        sleep(3);
    }
    return \@vocab;
}

sub print_vocab {
    my ($vocab, $csv_file) = @_;
    my $csv_fh = $csv_file->openw;
    for my $v (@$vocab) {
        say $csv_fh (join '|', @$v);
    }
}

sub clean_vocab {
    my ($input_file, $output_file) = @_;
    my @vocab;
    my @lines = $input_file->lines;
    my %all_vocab;
    OUTER: for my $line (@lines) {
        $line =~ s/\v//g;
        my ($rank, $thai, $english, $cat) = split /\|/, $line;
        next if !$rank or $rank > 6;
        # the categories need to be cleaned up a bit, and some of them I really don't care about
        $cat =~ s/[-\s]\(?\d\)?$//;
        $cat =~ s/^SOME IMPORTANT //;
        $cat =~ s/SOME/FEELINGS/;
        $cat =~ s/ VERBS//;
        $cat =~ s/ NOUNS//;
        # so many of the words are AUA category :((((((
        for my $no_thanks ('academic', 'abbrev', 'Thai ', 'Chapter', 'thai-provinces', 'MAANII', 'SHORT', 'LONG', 'CONSONANT', 'VOWEL') {
            if(index($cat, $no_thanks) != -1) {
                next OUTER;
            }
        }
        # only unique vocab
        next if $all_vocab{$thai}++;
        push @vocab, {cat => $cat, thai => $thai, english => $english, rank => $rank};
    }
    sort {$a->{cat} cmp $b->{cat} or $a->{rank} cmp $b->{rank}} @vocab;
    my $out_fh = $output_file->openw;
    for my $v (@vocab) {
        say $out_fh join '|', ($v->{cat}, $v->{rank}, $v->{thai}, $v->{english});
    }
}

my $destination_dir = path($ARGV[0]);

# my $cats = get_categories;
# my $vocab = download_vocab($cats);
# print_vocab($vocab, $destination_dir->child('vocab.csv'));

clean_vocab($destination_dir->child('vocab.csv'), $destination_dir->child('vocab_cleaned.csv'));
