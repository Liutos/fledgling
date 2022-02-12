;;; 私有的符号 BEGIN
(defun org-fledgling--make-command (program args)
  "生成以参数 ARGS 调用程序 PROGRAM 的命令。"
  (assert (stringp program))
  (dolist (arg args)
    (assert (or (numberp arg) (stringp arg))))

  (with-output-to-string
    (princ program)
    (dolist (arg args)
      (princ " ")
      (princ arg))))

(defun org-fledgling--run-fledgling (program args)
  "调用程序 fledgling，执行 ARGS 所指定的子命令。"
  (assert (stringp program))
  (dolist (arg args)
    (assert (or (numberp arg) (stringp arg))))

  (let ((command (org-fledgling--make-command program args)))
    (shell-command-to-string command)))
;;; 私有的符号 END

;;; 暴露的符号 BEGIN
(defvar *org-fledgling-program* nil
  "程序 fledgling 的可执行文件的路径。")
;;; 暴露的符号 END
