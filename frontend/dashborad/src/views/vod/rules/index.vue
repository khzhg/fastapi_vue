<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="源名称" prop="name">
        <el-input
          v-model="queryParams.name"
          placeholder="请输入源名称"
          clearable
          style="width: 240px;"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>

      <el-form-item label="源分组" prop="group">
        <el-select v-model="queryParams.group" filterable clearable placeholder="源分组" style="width: 240px">
          <el-option
            v-for="item in groupOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            :disabled="item.disabled">
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="文件类型" prop="file_type">
        <el-select v-model="queryParams.file_type" filterable clearable placeholder="文件类型" style="width: 240px">
          <el-option
            v-for="item in fileTypeOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            :disabled="item.disabled">
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="状态" prop="status">
        <el-select
          v-model="queryParams.status"
          placeholder="源状态"
          clearable
          style="width: 240px"
        >
          <el-option
            v-for="dict in statusOptions"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="success"
          icon="el-icon-refresh"
          size="mini"
          v-hasRole="['admin','opts']"
          @click="handleRefresh"
        >刷新源列表
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="el-icon-upload2"
          size="mini"
          v-hasPermi="['vod:rules:post']"
          @click="handleImport"
        >上传源文件
        </el-button>
      </el-col>

      <el-col :span="1.5">
        <el-button
          type="warning"
          icon="el-icon-delete"
          size="mini"
          v-hasRole="['admin','opts']"
          :disabled="multiple"
          @click="handleDelete"
        >删除数据
        </el-button>
      </el-col>

      <el-col :span="1.5">
        <el-button
          type="danger"
          icon="el-icon-delete"
          size="mini"
          v-hasRole="['admin','opts']"
          :disabled="multiple"
          @click="handleDeleteFiles"
        >删除文件
        </el-button>
      </el-col>

      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          v-hasRole="['admin','opts']"
          @click="handleClean"
        >清空数据
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          v-has-permi="['report:excel_generate:export','vod:rules:export']"
          @click="handleExport"
        >导出
        </el-button>
      </el-col>
    </el-row>

    <el-table ref="tables" v-loading="loading" :data="list" @selection-change="handleSelectionChange"
              :default-sort="defaultSort" @sort-change="handleSortChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="ID" align="center" prop="id" sortable="custom"
                       :sort-orders="['descending', 'ascending']"/>
      <el-table-column label="源名称" align="center" prop="name" width="200" :show-overflow-tooltip="true"
                       sortable="custom" :sort-orders="['descending', 'ascending']"/>
      <el-table-column label="源分组" align="center" prop="group" width="130" :show-overflow-tooltip="true"
                       :formatter="groupFormat"/>
      <el-table-column label="文件路径" align="center" prop="path" :show-overflow-tooltip="true" width="200"/>
      <el-table-column label="是否存在" align="center" prop="is_exist" width="100">
        <template slot-scope="scope">
          <el-switch v-model="scope.row.is_exist" disabled></el-switch>
        </template>
      </el-table-column>

      <el-table-column label="显示排序" align="center" prop="order_num"/>
      <el-table-column label="文件类型" align="center" prop="file_type"/>
      <el-table-column label="排序" align="center" prop="order_num" sortable="custom"
                       :sort-orders="['descending', 'ascending']"/>
      <!--      <el-table-column label="源状态" align="center" prop="status">-->
      <!--        <template slot-scope="scope">-->
      <!--          <dict-tag :options="statusOptions" :value="scope.row.status"/>-->
      <!--        </template>-->
      <!--      </el-table-column>-->

      <el-table-column label="源状态" align="center" prop="status" width="130" :show-overflow-tooltip="true"
                       :formatter="statusFormat"/>
      <el-table-column label="ext扩展" align="center" prop="ext" :show-overflow-tooltip="true"/>
      <el-table-column label="是否显示" align="center" prop="active" width="100">
        <template slot-scope="scope">
          <el-switch v-model="scope.row.active" @change="handleChangIsActive(scope.row)"></el-switch>
        </template>
      </el-table-column>

      <el-table-column label="创建时间" align="center" prop="created_ts" sortable="custom"
                       :sort-orders="['descending', 'ascending']" width="150">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.created_ts) }}</span>
        </template>
      </el-table-column>

      <el-table-column label="更新时间" align="center" prop="modified_ts" sortable="custom"
                       :sort-orders="['descending', 'ascending']" width="150">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.modified_ts) }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" align="center" class-name="small-padding fixed-width" width="240">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            v-hasPermi="['vod:rule:post']"
            @click="handleUpdate(scope.row)"
          >修改
          </el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            v-hasRole="['admin','opts']"
            @click="handleDelete(scope.row)"
          >删除
          </el-button>
          <el-dropdown size="mini" @command="(command) => handleCommand(command, scope.row)">
            <el-button size="mini" type="text" icon="el-icon-d-arrow-right">更多</el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="handleRun" icon="el-icon-menu" v-hasRole="['admin','opts']"
              >首页
              </el-dropdown-item>
              <el-dropdown-item command="handleView" icon="el-icon-search" v-hasRole="['admin','opts']"
              >搜索
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.page"
      :limit.sync="queryParams.page_size"
      @pagination="getList"
    />

    <!-- 添加或修改源对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="800px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="120px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="源状态" prop="status">
              <el-input v-model="form.status" placeholder="请输入源状态"/>
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="是否显示" prop="active">
              <el-switch v-model="form.active"></el-switch>
            </el-form-item>
          </el-col>

          <el-col :span="24">
            <el-form-item label="ext扩展" prop="ext">
              <el-input v-model="form.ext" placeholder="请输入源ext扩展" type="textarea"
                        :rows="5" clearable/>
            </el-form-item>
          </el-col>

        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 源导入对话框 -->
    <el-dialog :title="upload.title" :visible.sync="upload.open" width="400px" append-to-body>
      <el-upload
        ref="upload"
        multiple
        :limit="100"
        accept=".py, .json,.js,.txt,.m3u"
        :headers="upload.headers"
        :action="upload.url + '?updateSupport=' + upload.updateSupport + '&group=' + encodeURIComponent(upload.group)"
        :disabled="upload.isUploading"
        :on-progress="handleFileUploadProgress"
        :on-success="handleFileSuccess"
        :auto-upload="false"
        :on-change="uploadChange"
        :before-remove="beforeRemove"
        :on-remove="upLoadRemove"
        :file-list="upload.fileList"
        name="files"
        drag
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip text-center" slot="tip">
          <div class="el-upload__tip" slot="tip">
            源分组
            <el-select v-model="upload.group" filterable placeholder="源分组" style="width: 240px">
              <el-option
                v-for="item in groupOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
                :disabled="item.disabled">
              </el-option>
            </el-select>
          </div>

          <div class="el-upload__tip" slot="tip">
            <el-checkbox v-model="upload.updateSupport"/>
            是否更新已经存在的源
          </div>
          <span>仅允许导入分组对应格式的文件。</span>
        </div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitFileForm">确 定</el-button>
        <el-button @click="upload.open = false">取 消</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import {
  list,
  clearRecord,
  delRecord,
  refreshRules,
  changeActive,
  getRule,
  setRecord,
  uploadRules
} from "@/api/vod/rules";
import {getDicts} from "@/api/system/dict/data";
import {parseTime} from "@/utils";
import {getToken} from "@/utils/auth";

export default {
  name: "VodRules",
  // dicts: ['sys_common_status'],
  data() {
    return {
      // 遮罩层
      loading: true,
      // 选中数组
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 选择用户名
      selectName: "",
      // 显示搜索条件
      showSearch: true,
      // 总条数
      total: 0,
      // 表格数据
      list: [],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 日期范围
      dateRange: [],
      // 默认排序
      defaultSort: {prop: 'order_num', order: 'ascending'},
      statusOptions: [],
      groupOptions: [],
      fileTypeOptions: [{label: 'py', value: '.py'}, {label: 'json', value: '.json'}, {
        label: 'js',
        value: '.js'
      }, {label: 'txt', value: '.txt'}, {label: 'm3u', value: '.m3u'}],

      // 上传源参数
      upload: {
        // 是否显示弹出层
        open: false,
        // 弹出层标题
        title: "",
        fileList: [],
        // 是否禁用上传
        isUploading: false,
        // 是否更新已经存在的源
        updateSupport: true,
        // 源分组
        group: 't4/spiders',
        // 设置上传的请求头部
        headers: {Token: getToken(), 'Content-Type': 'multipart/form-data'},
        // 上传的地址
        url: process.env.VUE_APP_BASE_API + "vods/rules/file/uploadData"
      },
      // 查询参数
      queryParams: {
        page: 1,
        page_size: 10,
        name: undefined,
        group: 't4/spiders',
        status: undefined
      },
      // 表单参数
      form: {},
      // 表单校验
      rules: {
        status: [
          {required: true, message: "源状态不能为空，且只能为1/0", trigger: "blur"}
        ],
      }
    };
  },
  created() {
    this.getList();
    getDicts("vod_rule_status").then(response => {
      this.statusOptions = response.data.details;
    });

    getDicts("vod_rule_group").then(response => {
      this.groupOptions = response.data.details;
      this.groupOptions.forEach(item => {
        if (item.is_default) this.queryParams.group = item.value
      })
    });
  },
  methods: {
    /** 查询登录日志列表 */
    getList() {
      this.loading = true;
      if (!this.queryParams.status && typeof (this.queryParams.status) === 'string') {
        this.queryParams.status = undefined;
      }
      list(this.queryParams).then(response => {
          this.list = response.data.results
          this.total = response.data.total
          this.loading = false;
        }
      );

    },
    // 字典状态字典翻译
    groupFormat(row, column) {
      return this.selectDictLabel(this.groupOptions, row.group);
    },
    statusFormat(row, column) {
      return this.selectDictLabel(this.statusOptions, row.status);
    },
    // 取消按钮
    cancel() {
      this.open = false;
      this.reset();
    },
    // 表单重置
    reset() {
      this.form = {
        active: undefined,
        status: 1,
      };
      this.resetForm("form");
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.page = 1;
      this.getList();
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.dateRange = [];
      this.resetForm("queryForm");
      this.queryParams.page = 1;
      this.$refs.tables.sort(this.defaultSort.prop, this.defaultSort.order)
    },
    /** 多选框选中数据 */
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.id)
      this.single = selection.length != 1
      this.multiple = !selection.length
      this.selectName = selection.map(item => item.user_name);
    },
    /** 排序触发事件 */
    handleSortChange(column, prop, order) {
      this.queryParams.order_by = column.prop;
      this.queryParams.is_desc = column.order === 'descending';
      this.getList();
    },
    /** 删除数据按钮操作 */
    handleDelete(row) {
      const ids = row.id || this.ids
      this.$modal.confirm('是否确认删除ID为"' + ids + '"的数据项|不会删除文件？').then(function () {
        return delRecord(ids);
      }).then((response) => {
        this.getList();
        this.$modal.msgSuccess(response.msg);
      }).catch(() => {
      });
    },
    /** 删除文件按钮操作 */
    handleDeleteFiles(row) {
      const ids = row.id || this.ids
      this.$modal.confirm('是否确认删除ID为"' + ids + '"的数据项|文件会一起删除？').then(function () {
        return delRecord(ids, {with_file: true});
      }).then((response) => {
        this.getList();
        this.$modal.msgSuccess(response.msg);
      }).catch(() => {
      });
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const id = row.id || this.ids;
      getRule(id).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改源";
      });
    },
    /** 提交按钮 */
    submitForm: function () {
      this.$refs["form"].validate(valid => {
        if (valid) {
          if (this.form.id != undefined) {
            setRecord(this.form.id, this.form).then(response => {
              if (response.code === 0) {
                this.msgSuccess("修改成功")
                this.open = false
                this.getList()
              } else {
                this.msgError("修改失败," + response.msg)
              }
            })
          }
        }
      });
    },
    /** 刷新源列表按钮操作 */
    handleRefresh(row) {
      this.$modal.confirm('是否确认刷新本地所有源？').then(function () {
        return refreshRules();
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("刷新成功");
      }).catch(() => {
      });
    },
    /** 清空按钮操作 */
    handleClean() {
      this.$modal.confirm('是否确认清空所有源？').then(function () {
        return clearRecord();
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("清空成功");
      }).catch(() => {
      });
    },
    /** 改变活跃状态 */
    handleChangIsActive(row) {
      changeActive(row.id, row.active).then(response => {
        if (response.code === 0) {
          this.msgSuccess("修改成功")
        }
        this.getList();
      })
    },
    /** 导出按钮操作 */
    handleExport() {
      this.download('vod_rules', {
        ...this.queryParams, ...{template: '0'}
      }, `源列表_${parseTime(new Date().getTime())}.xlsx`)
    },
    /** 上传源文件按钮操作 */
    handleImport() {
      this.upload.title = "上传源文件";
      this.upload.open = true;
    },
    // 文件上传中处理
    handleFileUploadProgress(event, file, fileList) {
      this.upload.isUploading = true;
    },
    beforeRemove(file, fileList) {
      this.upload.fileList = fileList;
      // return this.$confirm(`确定移除 ${file.name}？`);
    },
    // 移除附件
    upLoadRemove(file, fileList) {
      let tempFileList = [];
      for (var index = 0; index < this.upload.fileList.length; index++) {
        if (this.upload.fileList[index].name !== file.name) {
          tempFileList.push(this.upload.fileList[index]);
        }
      }
      this.upload.fileList = tempFileList;
    },
    // 监控上传文件列表
    uploadChange(file, fileList) {
      let existFile = fileList.slice(0, fileList.length - 1).find((f) => f.name === file.name);
      if (existFile) {
        this.$message.error("当前文件已经存在!");
        fileList.pop();
      }
      this.upload.fileList = fileList;
    },
    // 上传到服务器  formidable接收
    async submitUpload() {
      // 上传文件大小不能超过2MB!
      const isLt2M = this.upload.fileList.every(
        (file) => file.size / 1024 / 1024 < 2
      );
      console.log('isLt2M:', isLt2M);
      if (!isLt2M) {
        this.$message({
          type: 'error',
          message: `请检查文件列表，不允许上传超过2mb的文件`
        });
        return
      }
      let formData = new FormData();
      // formData.files = this.upload.fileList.map(it => it.raw);
      this.upload.fileList.forEach(file => {
        formData.append('files', file.raw)
      });
      // console.log(formData);
      const response = await uploadRules(formData, {
        updateSupport: this.upload.updateSupport,
        group: this.upload.group
      });
      this.handleFileSuccess(response, null, null)
    },
    // 覆盖默认的上传行为
    requestUpload() {
      // :http-request="requestUpload"
    },
    // 文件上传成功处理
    handleFileSuccess(response, file, fileList) {
      this.upload.open = false;
      this.upload.isUploading = false;
      this.$refs.upload.clearFiles();
      this.$alert("<div style='overflow: auto;overflow-x: hidden;max-height: 70vh;padding: 10px 20px 0;'>" + response.msg + "</div>", "上传结果", {dangerouslyUseHTMLString: true});
      this.getList();
    },
    // 提交上传文件
    submitFileForm() {
      // this.$refs.upload.submit();
      this.submitUpload();
    },
  }
};
</script>
