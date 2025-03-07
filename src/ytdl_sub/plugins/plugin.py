from abc import ABC
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import final

from ytdl_sub.config.preset_options import Overrides
from ytdl_sub.entries.entry import Entry
from ytdl_sub.utils.file_handler import FileMetadata
from ytdl_sub.utils.logger import Logger
from ytdl_sub.validators.strict_dict_validator import StrictDictValidator
from ytdl_sub.ytdl_additions.enhanced_download_archive import DownloadArchiver
from ytdl_sub.ytdl_additions.enhanced_download_archive import EnhancedDownloadArchive


class PluginOptions(StrictDictValidator):
    """
    Class that defines the parameters to a plugin
    """

    # pylint: disable=no-self-use
    def added_source_variables(self) -> List[str]:
        """
        If the plugin adds source variables, list them here.

        Returns
        -------
        List of added source variables this plugin creates
        """
        return []

    # pylint: disable=unused-argument
    def validate_with_variables(
        self, source_variables: List[str], override_variables: List[str]
    ) -> None:
        """
        Optional validation after init with the session's source and override variables.

        Parameters
        ----------
        source_variables
            Available source variables when running the plugin
        override_variables
            Available override variables when running the plugin
        """
        return None

    # pylint: enable=no-self-use,unused-argument


PluginOptionsT = TypeVar("PluginOptionsT", bound=PluginOptions)


class Plugin(DownloadArchiver, Generic[PluginOptionsT], ABC):
    """
    Class to define the new plugin functionality
    """

    plugin_options_type: Type[PluginOptionsT] = NotImplemented

    @final
    def __init__(
        self,
        plugin_options: PluginOptionsT,
        overrides: Overrides,
        enhanced_download_archive: EnhancedDownloadArchive,
    ):
        DownloadArchiver.__init__(self=self, enhanced_download_archive=enhanced_download_archive)
        self.plugin_options = plugin_options
        self.overrides = overrides
        # TODO pass yaml snake case name in the class somewhere, and use it for the logger
        self._logger = Logger.get(self.__class__.__name__)

    def ytdl_options(self) -> Optional[Dict]:
        """
        Returns
        -------
        ytdl options to enable/disable when downloading entries for this specific plugin
        """

    # pylint: disable=no-self-use
    def modify_entry(self, entry: Entry) -> Optional[Entry]:
        """
        For each entry downloaded, modify the entry in some way before sending it to
        post-processing.

        Parameters
        ----------
        entry
            Entry to modify

        Returns
        -------
        The entry or None, indicating not to move it to the output directory
        """
        return entry

    # pylint: enable=no-self-use

    def post_process_entry(self, entry: Entry) -> Optional[FileMetadata]:
        """
        For each entry downloaded, apply post processing to it.

        Parameters
        ----------
        entry
            Entry to post process

        Returns
        -------
        Optional file metadata for the entry media file.
        """

    def post_process_subscription(self):
        """
        After all downloaded files have been post-processed, apply a subscription-wide post process
        """
