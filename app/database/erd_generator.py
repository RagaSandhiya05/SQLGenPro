import html

from graphviz import Digraph

from app.database.schema_intelligence import (
    get_database_schema,
    get_database_relationships,
)


def generate_erd():
    schema = get_database_schema()
    relationships = get_database_relationships(schema)

    diagram = Digraph(
        name="SQLGenPro_ERD",
        format="svg",
    )

    diagram.attr(
        rankdir="LR",
        bgcolor="#0E1117",
        pad="0.5",
        nodesep="0.8",
        ranksep="1.2",
        splines="spline",
    )

    diagram.attr(
        "node",
        shape="plain",
        fontname="Helvetica",
        fontcolor="#E2E8F0",
    )

    diagram.attr(
        "edge",
        color="#38BDF8",
        fontcolor="#CBD5E1",
        fontname="Helvetica",
        fontsize="10",
        penwidth="1.5",
        arrowsize="0.8",
    )

    # Map real table and column names to safe Graphviz identifiers.
    table_ids = {}
    column_ports = {}

    for table_index, (table_name, details) in enumerate(schema.items()):

        node_id = f"table_{table_index}"
        table_ids[table_name] = node_id

        rows = []

        # Table heading
        safe_table_name = html.escape(str(table_name))

        rows.append(
            '<TR>'
            '<TD COLSPAN="3" BGCOLOR="#1E293B">'
            '<FONT COLOR="#38BDF8" POINT-SIZE="12">'
            f'<B>{safe_table_name}</B>'
            '</FONT>'
            '</TD>'
            '</TR>'
        )

        column_ports[table_name] = {}

        for column_index, column in enumerate(details["columns"]):

            column_name = str(column["name"])
            port_id = f"port_{table_index}_{column_index}"

            column_ports[table_name][column_name] = port_id

            safe_column_name = html.escape(column_name)
            safe_column_type = html.escape(str(column["type"]))

            markers = []

            if column.get("primary_key"):
                markers.append("PK")

            if column.get("foreign_key"):
                markers.append("FK")

            if column.get("unique"):
                markers.append("UQ")

            if not column.get("nullable", True):
                markers.append("NN")

            marker_text = html.escape(" ".join(markers) or "-")

            rows.append(
                '<TR>'
                f'<TD ALIGN="LEFT" BGCOLOR="#111827" PORT="{port_id}">'
                f'<FONT COLOR="#FFFFFF">{safe_column_name}</FONT>'
                '</TD>'
                '<TD ALIGN="LEFT" BGCOLOR="#111827">'
                f'<FONT COLOR="#CBD5E1">{safe_column_type}</FONT>'
                '</TD>'
                '<TD ALIGN="LEFT" BGCOLOR="#111827">'
                f'<FONT COLOR="#38BDF8"><B>{marker_text}</B></FONT>'
                '</TD>'
                '</TR>'
            )

        label = (
            '<<TABLE BORDER="0" CELLBORDER="1" '
            'CELLSPACING="0" CELLPADDING="7" '
            'COLOR="#334155">'
            + "".join(rows)
            + '</TABLE>>'
        )

        diagram.node(node_id, label=label)

    # Add foreign-key relationships.
    for relation in relationships:

        source_table = relation["source_table"]
        target_table = relation["target_table"]

        if source_table not in table_ids or target_table not in table_ids:
            continue

        for source_column, target_column in zip(
            relation["source_columns"],
            relation["target_columns"],
        ):

            source_port = column_ports.get(
                source_table, {}
            ).get(source_column)

            target_port = column_ports.get(
                target_table, {}
            ).get(target_column)

            if not source_port or not target_port:
                continue

            diagram.edge(
                f'{table_ids[source_table]}:{source_port}',
                f'{table_ids[target_table]}:{target_port}',
                label="FK",
            )

    return diagram
