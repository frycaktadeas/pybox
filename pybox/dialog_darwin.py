from typing import List, Union, Tuple
from dialog import Dialog
import subprocess


class DialogDarwin(Dialog):
    """
    Implementation of dialogs from MacOS (Python wrapper for AppleScript)
    Docs: https://applescript.fandom.com/wiki/Category:User_Interaction
    By: Tadeáš Fryčák (@frycaktadeas on GitHub)
    """

    DEBUG = True

    @staticmethod
    def __run(command):
        return subprocess.run(["osascript", "-e", command], capture_output=True)

    def __run_to_json(self, message: List[str]):
        """
        Parse output from AppleScript
        TODO - implement more robust approach (", " or ":" could be in entry, and so on)
        :param message: str
        :return: JSON
        """
        json = {}
        output = self.__run(" ".join(message)).stdout.decode().strip()

        if self.DEBUG:
            print(output)

        if output:
            if ":" in output:
                for v in output.split(", "):
                    key = v.split(":")[0]
                    if "alias macintosh" in key.lower():
                        return output.replace(":", "/").replace("alias Macintosh HD", "").split(", ")
                    else:
                        value = "/".join(v.split(":")[1:])
                        value = False if value == "false" else True if value == "true" else value

                        json[key.replace(" ", "_")] = value
            else:
                return output.split(", ") if "," in output else [output]
        return json

    @staticmethod
    def __bool(message):
        return str(message).lower()

    @staticmethod
    def __list(message):
        return str(message).replace("[", "{").replace("]", "}").replace("'", '"')

    def __create_command(self, dialog_type, title: str = None, prompt: str = None, default_answer: str = None,
                         hidden_answer: bool = False, buttons: List[str] = None, default_button: str = None,
                         cancel_button: str = None, icon: str = None, give_up_after: int = None, as_type: str = None,
                         default_location: str = None, default_name: str = None, multiple_selection: bool = False,
                         show_package_content: bool = False, invisible: bool = False, empty_selection: bool = False,
                         default_items: Union[List, str, int] = None, ok_button_name: str = None,
                         cancel_button_name: str = None, showing: List[str] = None, editable_url: bool = False,
                         message: str = None, types: List[str] = None, default_color: Tuple[int] = None):
        string = [dialog_type]

        if title is not None:
            string.append(f'with title "{title}"')

        if prompt is not None:
            string.append(f'with prompt "{prompt}"')

        if message is not None:
            string.append(f'with message "{message}"')

        if default_answer is not None:
            string.append(f'default answer "{default_answer}"')

        if hidden_answer:
            string.append(f'hidden answer {self.__bool(hidden_answer)}')

        if buttons is not None:
            assert isinstance(buttons, list), "Buttons not a list"
            string.append(f'buttons {self.__list(buttons)}')

        if default_button is not None:
            assert default_button in buttons, f"Button {default_button} is not in buttons"
            string.append(f'default button "{default_button}"')

        if cancel_button is not None:
            assert default_button in buttons, f"Button {default_button} is not in buttons"
            string.append(f'cancel button "{cancel_button}"')

        if icon is not None:  # could be path, ID, or caution, stop, note
            # assert icon in ["caution", "stop", "note"].extend(range(3)), "Icon argument invalid"
            string.append(f'with icon {icon}')

        if give_up_after is not None:
            string.append(f"giving up after {give_up_after}")

        if as_type is not None:
            assert as_type in ["critical", "informational", "warning"], "as_type invalid"
            string.append(f'as {as_type}')

        if default_location is not None:
            string.append(f'default location "{default_location}"')

        if default_name is not None:
            string.append(f'default name "{default_name}"')

        if default_color is not None:
            string.append(f'default color {self.__list(default_color)}')

        if multiple_selection:
            string.append(f'multiple selections allowed {self.__bool(multiple_selection)}')

        if show_package_content:
            string.append(f'showing package contents {self.__bool(show_package_content)}')

        if invisible:
            string.append(f'invisibles {self.__bool(invisible)}')

        if empty_selection:
            string.append(f'empty selection allowed {self.__bool(empty_selection)}')

        if editable_url:
            string.append(f'editable URL {self.__bool(editable_url)}')

        if default_items is not None:
            if isinstance(default_items, list):
                string.append(f'default items {self.__list(default_items)}')
            else:
                string.append(f'default items {default_items}')

        if types is not None:
            string.append(f'of type {self.__list(types)}')

        if ok_button_name is not None:
            string.append(f'OK button name {ok_button_name}')

        if cancel_button_name is not None:
            string.append(f'cancel button name "{cancel_button_name}"')

        if showing is not None:
            string.append(f'cancel button name "{self.__list(cancel_button_name)}"')

        if self.DEBUG:
            print(string)

        return self.__run_to_json(string)

    def message_box(self, content: str, title=None, buttons: List[str] = None, icon: str = None,
                    default_button: Union[str, int] = None, cancel_button: Union[str, int] = None,
                    give_up_after: int = None):
        """
        Trigger message box
        :param content: content of window
        :param title: title of window
        :param buttons: list of button names
        :param icon: caution/stop/note or ID of icon (0, 1, 2) or path to icon
        :param default_button: name of default button from buttons
        :param cancel_button: name of cancel button from buttons
        :param give_up_after: close after x seconds
        :return: JSON output
        """
        return self.__create_command(
            f'display dialog "{content}"', title=title, buttons=buttons, default_button=default_button,
            cancel_button=cancel_button, give_up_after=give_up_after, icon=icon
        )

    def ask_question(self, content: str, title=None, default_answer: str = "", buttons: List[str] = None,
                     icon: str = None, default_button: Union[str, int] = None, cancel_button: Union[str, int] = None,
                     give_up_after: int = None):
        """
        Trigger message box with entry
        :param content: content of window
        :param title: title of window
        :param buttons: list of button names
        :param icon: caution/stop/note or ID of icon (0, 1, 2) or path to icon
        :param default_answer: default answer filled in entry
        :param default_button: name of default button from buttons
        :param cancel_button: name of cancel button from buttons
        :param give_up_after: close after x seconds
        :return: JSON output
        """
        return self.__create_command(
            f'display dialog "{content}"', title=title, default_answer=default_answer, buttons=buttons,
            default_button=default_button, cancel_button=cancel_button, give_up_after=give_up_after, icon=icon
        )

    def ask_password(self, content: str, title=None, default_answer: str = "", buttons: List[str] = None,
                     icon: str = None, default_button: Union[str, int] = None, cancel_button: Union[str, int] = None,
                     give_up_after: int = None):
        """
        Trigger message box with hidden content in entry
        :param content: content of window
        :param title: title of window
        :param buttons: list of button names
        :param icon: caution/stop/note or ID of icon (0, 1, 2) or path to icon
        :param default_answer: default answer filled in entry
        :param default_button: name of default button from buttons
        :param cancel_button: name of cancel button from buttons
        :param give_up_after: close after x seconds
        :return: JSON output
        """
        return self.__create_command(
            f'display dialog "{content}"', title=title, default_answer=default_answer, buttons=buttons,
            default_button=default_button, cancel_button=cancel_button, give_up_after=give_up_after, icon=icon,
            hidden_answer=True
        )

    def alert_box(self, title: str, content: str = None, buttons: List = None, as_type: str = None,
                  default_button: str = None, cancel_button: str = None, give_up_after: int = None):
        """
        Show alert box to user
        :param title: title of window
        :param content: message content
        :param buttons: list of buttons
        :param as_type: critical/"informational/warning
        :param default_button: name of default button from buttons
        :param cancel_button: name of cancel button from buttons
        :param give_up_after: close after x seconds
        :return: JSON output
        """
        return self.__create_command(
            f"display alert {title}", message=content, as_type=as_type, buttons=buttons, default_button=default_button,
            cancel_button=cancel_button, give_up_after=give_up_after
        )

    def ask_file(self, title: str = None, types: List[str] = None, default_location: str = None,
                 invisible: bool = False, multiple_selection: bool = False, show_package_content: bool = False):
        """
        Ask for file input from user
        :param title: title of window
        :param types: types of extensions, e.g. ["pdf", "jpg"]
        :param default_location: default folder/dir location
        :param invisible: show invisible files/dirs (True/False)
        :param multiple_selection: True/False
        :param show_package_content: True/False
        :return:
        """
        return self.__create_command(
            "choose file", prompt=title, types=types, default_location=default_location, invisible=invisible,
            multiple_selection=multiple_selection, show_package_content=show_package_content
        )

    def ask_filename(self, title: str = None, default_name: str = None, default_location: str = None):
        """
        Ask for filename input from user
        :param title: title of window
        :param default_name: default name of file
        :param default_location: default folder/dir location
        :return: output JSOn
        """
        return self.__create_command(
            "choose file name", prompt=title, default_name=default_name, default_location=default_location
        )

    def ask_directory(self, title: str = None, default_location: str = None, invisible: bool = False,
                      multiple_selection: bool = False, show_package_content: bool = False):
        """
        Ask for directory/folder input from user
        :param title: title of window
        :param default_location: initial location
        :param invisible: show invisible files/dirs (True/False)
        :param multiple_selection: True/False
        :param show_package_content: True/False
        :return: output JSON
        """
        return self.__create_command(
            "choose folder", prompt=title, default_location=default_location, invisible=invisible,
            multiple_selection=multiple_selection, show_package_content=show_package_content
        )

    def ask_from_list(self, items: List, title: str = None, prompt: str = None,
                      default_items: Union[List, str, int] = None, ok_button_name: str = None,
                      cancel_button_name: str = None, multiple_selection: bool = False,
                      show_package_content: bool = False):
        """
        Ask for item selection from list from user
        :param items: items to select from
        :param title: title of window
        :param prompt: label in window
        :param default_items: initially selected items # TODO Apple bug - showing parameter does not work for length > 1
        :param ok_button_name: name of OK button
        :param cancel_button_name: name of cancel button
        :param multiple_selection: True/False
        :param show_package_content: True/False
        :return: JSON output
        """

        return self.__create_command(
            f"choose from list {self.__list(items)}", title=title, prompt=prompt, default_items=default_items,
            ok_button_name=ok_button_name, cancel_button_name=cancel_button_name, multiple_selection=multiple_selection,
            show_package_content=show_package_content
        )

    def ask_color(self, default_color: Tuple[int, int, int] = None):
        """
        Ask for color selection from user
        :param default_color: default 16bit RGB color (e.g. (65000, 0, 300))
        :return: JSON output
        """
        return self.__create_command("choose color", default_color=default_color)

    def ask_application(self, title: str = None, prompt: str = None, multiple_selection: bool = False, as_type=None):
        """
        Ask for application selection from user
        :param title: title of window
        :param prompt: label in window
        :param multiple_selection: True/False
        :param as_type: # TODO not implemented yet
        :return: JSON output
        """
        return self.__create_command(
            "choose application", title=title, prompt=prompt, multiple_selection=multiple_selection
        )

    def ask_remote_application(self, title: str = None, prompt: str = None):
        """
        Ask for remote application selection from user
        :param title: title of window
        :param prompt: label in window
        :return: JSON output
        """
        return self.__create_command("choose remote application", title=title, prompt=prompt)

    def ask_url(self, showing: List[str] = None, editable_url: bool = False):
        """
        Ask for URL selectino from user
        :param showing: TODO bug showing does not work
        :param editable_url: can user edit the URL?
        :return: JSON output
        """
        return self.__create_command("choose URL", showing=showing, editable_url=editable_url)

    def beep(self, count: int):
        """
        Trigger MacOS built-in beep
        :param count: count of beeps
        :return: JSON output
        """
        return self.__create_command(f"beep {count}")


if __name__ == "__main__":
    dd = DialogDarwin()

    print(dd.message_box("Hello", "Content", icon="stop"))
