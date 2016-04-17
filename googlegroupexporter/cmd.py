from googlegroupexporter.cli import arguments, verbosity, export_with_progress
from googlegroupexporter.exporters import CsvExporter, MailExporter
from googlegroupexporter.session import session_factory


def main():
    options = arguments()

    verbosity(options.verbose)

    session = session_factory(
        options.cookies, options.workers,
        options.cache_dir, options.cache_days, options.cache_forever
    )

    # Choose exporter class according to selected mode.
    Exporter = dict(csv=CsvExporter, mbox=MailExporter)[options.mode]

    export_with_progress(Exporter(session), options.group)
