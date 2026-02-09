# 分支管理与开发规范
## 一、长期分支
- main：生产环境分支，受保护，仅通过 PR 合并
- develop：开发集成分支，日常开发合并入口

## 二、短期分支
- feature/*：功能分支，格式：feature/模块名-功能简述
- hotfix/*：紧急修复分支，格式：hotfix/问题描述-日期
- bugfix/*：普通bug修复分支
- release/*：发布分支，格式：release/v1.0.0

## 三、命名规范
- 全部小写英文
- 使用连字符 - 分隔
- 长度不超过50字符
- 语义清晰，一目了然

## 四、功能开发流程
1. 从 develop 分支拉取最新代码
git checkout develop
git pull origin develop

2. 创建新功能分支
git checkout -b feature/模块名-功能名

3. 开发中定期提交
git add .
git commit -m "feat(模块): 功能描述"

4. 推送至远程
git push origin feature/分支名

5. 提交 PR 合并到 develop
- 目标分支：develop
- 至少1人CodeReview
- 通过CI/CD检查后合并

## 五、Commit 信息规范
- feat：新功能
- fix：bug修复
- docs：文档更新
- style：格式、标点、空格调整
- refactor：重构
- test：测试相关
- chore：构建、工具、依赖变动

示例：
feat(ai-model): 集成Stable Diffusion API
fix(user): 修复登录状态失效问题

## 六、代码合并规则
- Squash and Merge：功能分支合并
- Rebase and Merge：hotfix 分支合并
- Create a Merge Commit：release 发布分支合并
