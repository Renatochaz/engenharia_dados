"""Class to deserialize NFe json documents into pandas.DataFrame.

@author: Renato Chavez
"""

import os
from typing import Union
import json
import pandas as pd


class NFeJsonDeserializer():
    """Deserialize NFe json into `pandas.DataFrame`.

    The JSON document is split between a "nfe_info" dataframe with
    the nfe information data, and a "item_list" dataframe with
    expanded ItemList information containing a relational NFeID.

    Args:
        data_path(str): PATH to the directory with NFe json data.
            Use the absolute PATH if runned by a python script, or
            the relative PATH if runned by a Jupyter Notebook.
        key(str, optional): Name of the column with the NFeID.
            Defaults to "NFeID".
    """

    def __init__(
        self,
        data_path: str,
        key: str = "NFeID"):

        self._path = data_path
        self._key = key

    def get_dataframe(
        self,
        filename: str,
        dataframe: str = "all") -> Union[pd.DataFrame, tuple]:
        """Deserialize a JSON document into a `pd.DataFrame`.

        The JSON document is split between a "nfe_info" dataframe with
        the nfe information data, and a "item_list" dataframe with
        expanded ItemList information containing a relational NFeID.

        Args:
            filename(str):  Name of the JSON which will be deserialized
                into the split `pandas.DataFrame`.
            dataframe(str): Name of the `pandas.DataFrame` to return.
                Use "nfe_info" to return the nfe_info dataframe, or
                "item_list" to return the item_list dataframe.
                Defaults to "all", which brings the two dataframes
                packed into a `tuple`.
        
        Returns:
            A `tuple` containing the JSON document deserialized into
            two `pandas.DataFrame`, or a single `pandas.DataFrame` if
            the optional argument "dataframe" was referenced.
        """

        if dataframe == "all":
            return tuple(self._split_data(filename).values())

        return self._split_data(filename)[dataframe]

    def list_files(self) -> list:
        """List all files contained in the "self._path" directory."""

        return os.listdir(self._path)

    def _split_data(self, filename: str) -> dict:
        """Split a `dictionary` with the NFe JSON document
        into a "nfe_info" dataframe with the nfe information data,
        and a "item_list" dataframe with expanded ItemList information
        containing a relational NFeID.

        Args:
            filename(str): Name of the JSON which will be deserialized
                into the split pandas.DataFrame.

        Returns:
            A `dictionary` with the nfe_info dataframe as value
            from a "nfe_info" key, and the itemlist dataframe
            as value from a "item_list" key.
        """

        itemlist = pd.DataFrame()

        nfe_info = pd.DataFrame(
            self._read_data(filename)
            ).drop("ItemList", axis=1)

        agg_itemlist = pd.DataFrame(
            self._read_data(filename)
            ).loc[:, ["NFeID", "ItemList"]]

        # Iterate over agg_itemlist dataframe and expand the
        # ItemList column, adding the corresponding self._key to the dataframe.
        for key in agg_itemlist[self._key]:
            open_itemlist = pd.json_normalize(
                    agg_itemlist.loc[
                        agg_itemlist[self._key] == key
                        ].explode("ItemList")["ItemList"]
                        )

            open_itemlist.insert(loc=0, column=self._key, value=key)
            itemlist = pd.concat([itemlist, open_itemlist])

        return {"nfe_info":nfe_info, "item_list": itemlist}

    def _read_data(self, filename: str) -> dict:
        """Deserialize a JSON document to a Python `dictionary`.

        Args:
            filename(str): Name of the JSON document to deserialize.

        Returns:
            A python `dictionary` with the JSON document.
        """

        path = os.path.join(self._path, filename)
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
